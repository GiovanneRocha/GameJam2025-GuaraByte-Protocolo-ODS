# -*- coding: utf-8 -*-
import sys, os, random
import pygame
from pygame.locals import QUIT, KEYDOWN
import settings as S
from levels import LEVELS
from utils import draw_grid_background, clamp
from ui import draw_hud, draw_boss_banner, draw_instructions
from entities import WordEnemy, Boss
import assets

try:
    from PIL import Image
except Exception:
    Image = None


class Game:
    def __init__(self, record_demo_seconds: int | None = None):
        pygame.init()
        
        # Inicialização do áudio
        try:
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
            pygame.mixer.music.set_volume(S.MUSIC_VOLUME)
        except Exception as e:
            print(f"Erro ao inicializar áudio: {e}")
        
        info = pygame.display.Info()
        max_h = int(info.current_h * 0.92)
        h = max(min(max_h, 960), 720)
        w = int(h * 9/16)

        self.is_fullscreen = False
        self.last_window_size = (S.WIDTH, S.HEIGHT)

        # create initial window (resizable)
        self.screen = self.create_window(self.last_window_size, fullscreen=False)

        self.clock = pygame.time.Clock()

        assets.load_assets()

        self.wallpaper = None
        self._wallpaper_scaled = None 
        self.music_path = None

        self.record_seconds = record_demo_seconds
        self.record_frames = []
        self.autoplay = record_demo_seconds is not None

        self.level_index = 0
        self.score = 0
        self.corrupcao = S.CORRUPCAO_INICIAL
        self.enemies: list[WordEnemy] = []
        self.target_enemy: WordEnemy | None = None
        self.current_input = ""
        self.spawn_t = 0.0
        self.spawn_interval = 1.0
        self.boss: Boss | None = None
        self.game_over = False
        self.victory = False

        self.begin_level(self.level_index)

        # Inicia música de fundo padrão
        assets.play_music('background.mp3')

    def create_window(self, size: tuple[int, int], fullscreen: bool = False):
        flags = pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE
        screen = pygame.display.set_mode(size, flags)
        # Recalcula runtime e escala; preserva DEMO_DIR definido anteriormente
        S.init_runtime(screen.get_width(), screen.get_height(), S.DEMO_DIR)
        pygame.display.set_caption(S.TITLE)
        return screen

    def begin_level(self, i: int):
        cfg = LEVELS[i]
        self.enemies = []
        self.target_enemy = None
        self.current_input = ""
        self.spawn_t = 0.0

        base = S.BASE_SPAWN_INTERVAL
        self.spawn_interval = max(S.MIN_SPAWN_INTERVAL, base / max(0.1, cfg.spawn_factor))
        if cfg.has_boss:
            self.boss = Boss(cfg.boss_words, cfg.boss_health)
        else:
            self.boss = None

        # --- carregamento gráfico / áudio da fase ---
        # wallpaper: cfg pode ser uma string com caminho relativo (ex: 'wall1.png' ou 'img/wall1.png')
        self.wallpaper = None
        self._wallpaper_scaled = None
        if getattr(cfg, 'wallpaper', None):
            # tenta recuperar por chave/arquivo via assets (aceita 'wallpaper4.png' ou 'assets/images/wallpaper4.png')
            try:
                img = assets.get_image(cfg.wallpaper)
                if img is None:
                    img = assets.load_image(cfg.wallpaper)
                self.wallpaper = img
            except Exception:
                self.wallpaper = None

        # música: cfg pode conter caminho para arquivo de áudio
        if getattr(cfg, 'music', None):
            ok = assets.play_music(cfg.music, getattr(cfg, 'music_volume', 0.6))
            if ok:
                self.music_path = cfg.music
            else:
                self.music_path = None
        else:
            assets.stop_music()
            self.music_path = None

    def destroy_all_with_word(self, word: str) -> int:
        removed = 0
        for e in list(self.enemies):
            if e.word == word:
                self.enemies.remove(e)
                removed += 1
        return removed

    def choose_enemy_by_prefix(self, prefix: str):
        candidates = [e for e in self.enemies if e.starts_with(prefix)]
        if not candidates:
            return None
        candidates.sort(key=lambda e: e.y, reverse=True)
        return candidates[0]

    def handle_key_char(self, ch: str):
        cfg = LEVELS[self.level_index]

        if (self.boss and not self.boss.defeated) and (not self.current_input) and (self.target_enemy is None):
            candidate = self.choose_enemy_by_prefix(ch)
            if candidate:
                self.target_enemy = candidate
                self.current_input = ch
            else:
                ok_b, completed, completed_word = self.boss.handle_char(ch)
                if ok_b:
                    assets.play('ok')
                if completed and completed_word:
                    # remove any minions with the same word (como em WordEnemy)
                    removed = self.destroy_all_with_word(completed_word)
                    if removed > 0:
                        self.score += 10 * removed
                        assets.play('clean')
                self.current_input += ch
        else:
            # normal flow
            if self.boss and not self.boss.defeated and self.target_enemy is None:
                ok_b, completed, completed_word = self.boss.handle_char(ch)
                if ok_b:
                    assets.play('ok')
                if completed and completed_word:
                    removed = self.destroy_all_with_word(completed_word)
                    if removed > 0:
                        self.score += 10 * removed
                        assets.play('clean')
                self.current_input += ch
            else:
                self.current_input += ch

    def update_logic(self, dt):
        if self.game_over or self.victory:
            return
        cfg = LEVELS[self.level_index]

        # Natural spawn
        self.spawn_t += dt
        if self.boss and not self.boss.defeated:
            # boss minions
            self.boss.update(dt)
            if self.boss.should_spawn_minion():
                self.enemies.append(WordEnemy(cfg.words, speed_factor=cfg.speed_factor))
                self.boss.reset_spawn()
        else:
            if self.spawn_t >= self.spawn_interval:
                self.spawn_t = 0.0
                self.enemies.append(WordEnemy(cfg.words, speed_factor=cfg.speed_factor))

        # Autoplay typing
        if self.autoplay:
            ch = None
            # prefer lowest enemy; else boss
            if self.enemies:
                if self.target_enemy:
                    idx = self.target_enemy.matched
                    if idx < len(self.target_enemy.word):
                        ch = self.target_enemy.word[idx]
                else:
                    # start a new target by first letter of lowest enemy
                    e = max(self.enemies, key=lambda x: x.y)
                    ch = e.word[0]
            elif self.boss and not self.boss.defeated and self.boss.current:
                idx = self.boss.matched
                if idx < len(self.boss.current):
                    ch = self.boss.current[idx]
            if ch:
                self.handle_key_char(ch)

        # Targeting for enemies (prefix mode)
        if (not (self.boss and not self.boss.defeated)) or (self.target_enemy is not None):
            if not self.target_enemy and self.current_input:
                self.target_enemy = self.choose_enemy_by_prefix(self.current_input)
            if self.target_enemy and self.current_input:
                if not self.target_enemy.starts_with(self.current_input):
                    self.current_input = ""
                    self.target_enemy.matched = 0
                    self.target_enemy = None
                else:
                    if self.current_input == self.target_enemy.word:
                        word = self.target_enemy.word
                        removed = self.destroy_all_with_word(word)
                        self.target_enemy = None
                        self.current_input = ""
                        if removed > 0:
                            # 10 pts por palavra removida
                            self.score += 10 * removed
                            assets.play('clean')

        # Update enemies
        for e in list(self.enemies):
            e.update(dt)
            if e.is_off_bottom():
                self.enemies.remove(e)
                self.corrupcao -= S.CORRUPCAO_PERDA
                if e == self.target_enemy:
                    self.target_enemy = None
                    self.current_input = ""

        # Check game over
        if self.corrupcao <= 0:
            self.game_over = True

        # Level progression: need score >= 300 and (if boss) boss defeated
        if cfg.has_boss:
            if (self.score >= cfg.target_score) and self.boss and self.boss.defeated:
                self.advance_level()
        else:
            if self.score >= cfg.target_score:
                self.advance_level()

    def advance_level(self):
        self.level_index += 1
        if self.level_index >= len(LEVELS):
            self.victory = True
        else:
            self.begin_level(self.level_index)

    def draw(self):
        cfg = LEVELS[self.level_index]

        # draw wallpaper se houver (redimensiona mantendo qualidade)
        if self.wallpaper:
            if (self._wallpaper_scaled is None) or (self._wallpaper_scaled.get_width() != S.WIDTH) or (self._wallpaper_scaled.get_height() != S.HEIGHT):
                try:
                    self._wallpaper_scaled = pygame.transform.smoothscale(self.wallpaper, (S.WIDTH, S.HEIGHT))
                except Exception:
                    self._wallpaper_scaled = pygame.transform.scale(self.wallpaper, (S.WIDTH, S.HEIGHT))
            if self._wallpaper_scaled:
                self.screen.blit(self._wallpaper_scaled, (0, 0))
        else:
            # se não há wallpaper, desenha grid normal de fundo
            draw_grid_background(self.screen, cfg.bg_color, cfg.grid_color)

        # enemies
        for e in self.enemies:
            e.draw(self.screen)
        # HUD
        hud_h = draw_hud(self.screen, cfg, self.score, self.corrupcao)
        # Boss banner
        top_after_boss = draw_boss_banner(self.screen, self.boss, hud_h)
        # Input + instructions
        draw_instructions(self.screen, self.current_input)

        # End states
        if self.game_over:
            f = pygame.font.Font(None, int(36 * S.SCALE))
            t = f.render(f"REDE CORROMPIDA! (Depurados: {self.score})", True, S.COLOR_TEXT_ERROR)
            r = t.get_rect(center=(S.WIDTH // 2, S.HEIGHT // 2))
            self.screen.blit(t, r)
        if self.victory:
            f = pygame.font.Font(None, int(36 * S.SCALE))
            t = f.render("MISSAO CUMPRIDA! REDE RESTAURADA.", True, (140, 255, 190))
            r = t.get_rect(center=(S.WIDTH // 2, S.HEIGHT // 2))
            self.screen.blit(t, r)

    def run(self):
        elapsed = 0.0
        running = True
        while running:
            dt = self.clock.tick(S.FPS) / 1000.0
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    running = False

                elif ev.type == pygame.VIDEORESIZE:
                    # usuário redimensionou a janela (só se não estiver em fullscreen)
                    if not self.is_fullscreen:
                        self.last_window_size = (ev.w, ev.h)
                        # recria a janela resizável com novo tamanho
                        self.screen = self.create_window(self.last_window_size, fullscreen=False)
                        # Se houver caches/surfaces dependentes do tamanho, recrie-os aqui.

                elif ev.type == KEYDOWN:
                    # teclas de controle
                    if ev.key == pygame.K_ESCAPE:
                        running = False
                    elif ev.key == pygame.K_F11:
                        # toggle fullscreen
                        if not self.is_fullscreen:
                            info = pygame.display.Info()
                            self.screen = self.create_window((info.current_w, info.current_h), fullscreen=True)
                            self.is_fullscreen = True
                        else:
                            self.screen = self.create_window(self.last_window_size, fullscreen=False)
                            self.is_fullscreen = False
                    else:
                        # input do jogador (somente quando jogando)
                        if not (self.game_over or self.victory):
                            # DELETE: remove a palavra inteira (target ou por input)
                            if ev.key == pygame.K_DELETE:
                                word = None
                                if self.target_enemy:
                                    word = self.target_enemy.word
                                elif self.current_input:
                                    cand = self.choose_enemy_by_prefix(self.current_input)
                                    word = cand.word if cand else None

                                if word:
                                    removed = self.destroy_all_with_word(word)
                                    # limpa estado de seleção/input
                                    self.current_input = ""
                                    self.target_enemy = None
                                    if removed > 0:
                                        self.score += 10 * removed
                                        assets.play('clean')
                                else:
                                    # nada para deletar: apenas limpa o input
                                    self.current_input = ""

                            else:
                                ch = ev.unicode.upper() if hasattr(ev, 'unicode') else ''
                                if ch and ch.isprintable() and len(ch) == 1 and ch.isalnum():
                                    self.handle_key_char(ch)
                                elif ev.key == pygame.K_BACKSPACE:
                                    self.current_input = self.current_input[:-1]
                                    if not self.current_input and self.target_enemy:
                                        self.target_enemy = None

            self.update_logic(dt)
            self.draw()

            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':

    secs = None
    if len(sys.argv) >= 3 and sys.argv[1] == '--record-demo':
        try:
            secs = int(sys.argv[2])
        except Exception:
            secs = 10
    Game(record_demo_seconds=secs).run()
