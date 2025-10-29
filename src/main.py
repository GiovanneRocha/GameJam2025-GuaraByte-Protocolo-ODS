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
from menu import Menu
from cutscene import Cutscene
from credits import Credits

try:
    from PIL import Image
except Exception:
    Image = None


class Game:
    def __init__(self, record_demo_seconds: int | None = None):
        pygame.init()
        
        try:
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
            pygame.mixer.music.set_volume(S.MUSIC_VOLUME)
        except Exception as e:
            print(f"Erro ao inicializar áudio: {e}")
        
        # Usa dimensões definidas em settings
        self.is_fullscreen = False
        self.last_window_size = (S.WINDOW_WIDTH, S.WINDOW_HEIGHT)
        self.screen = self.create_window(self.last_window_size, fullscreen=False)

        self.clock = pygame.time.Clock()

        assets.load_assets()

        # menu / cutscene
        self.menu = Menu(self)
        self.cutscene = Cutscene(self, slides=None)
        self.credits = Credits(self)
        # estado: 'menu' | 'cutscene' | 'playing' | 'credits' | 'victory'
        self.state = 'menu'

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

        # Inicia música de fundo padrão (mas menu pode substituir)
        assets.play_music('background.mp3')

    def create_window(self, size: tuple[int, int], fullscreen: bool = False):
        if fullscreen:
            size = (S.FULLSCREEN_WIDTH, S.FULLSCREEN_HEIGHT)
        flags = pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE
        screen = pygame.display.set_mode(size, flags)
        S.init_runtime(screen.get_width(), screen.get_height(), S.DEMO_DIR)
        pygame.display.set_caption(S.TITLE)
        return screen

    def begin_level(self, i: int):
        # Remove verificação de cutscene aqui, já que ela é iniciada no menu
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
                    # som de dano no boss
                    try:
                        assets.play('boss_hit')   # coloque assets/sounds/boss_hit.wav
                    except Exception:
                        try:
                            assets.play('ok')
                        except Exception:
                            pass
                if completed and completed_word:
                    # remove any minions with the same word (como em WordEnemy)
                    removed = self.destroy_all_with_word(completed_word)
                    # limpa a palavra corrente do boss (comportamento igual aos vírus)
                    try:
                        if hasattr(self.boss, 'clear_current'):
                            self.boss.clear_current()
                        else:
                            # fallback: zera matched/current se existir
                            if hasattr(self.boss, 'current'):
                                self.boss.current = ""
                            if hasattr(self.boss, 'matched'):
                                self.boss.matched = 0
                    except Exception:
                        pass
                    if removed > 0:
                        self.score += 10 * removed
                        assets.play('clean')
                    # if the boss was defeated by this input, trigger victory visuals immediately
                    if self.boss and getattr(self.boss, 'defeated', False):
                        try:
                            self.show_victory()
                        except Exception:
                            pass
                        return
                    # after completing a boss word, reset player input and target
                    self.current_input = ""
                    self.target_enemy = None
                    return
                # append only when not completing the boss word
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
                    # if the boss was defeated by this input, trigger victory visuals immediately
                    if self.boss and getattr(self.boss, 'defeated', False):
                        try:
                            self.show_victory()
                        except Exception:
                            pass
                        return
                    # reset the input box when boss word completed
                    self.current_input = ""
                    self.target_enemy = None
                    return
                # append only when not completing the boss word
                self.current_input += ch
            else:
                self.current_input += ch

    def show_victory(self):
        """Chamada quando derrotar o boss final"""
        self.victory = True
        # Toca música de vitória (use assets/musics/victory.mp3)
        try:
            assets.play_music('musics/victory.mp3', getattr(S, 'MUSIC_VOLUME', 0.6))
        except Exception:
            try:
                assets.play_music('victory.mp3', getattr(S, 'MUSIC_VOLUME', 0.6))
            except Exception:
                pass

        # Partículas / efeitos visuais de vitória
        self.victory_timer = 5.0  # segundos antes dos créditos
        self.victory_particles = []
        import random
        for i in range(80):
            self.victory_particles.append({
                'x': random.uniform(0, S.WIDTH),
                'y': random.uniform(-S.HEIGHT*0.2, S.HEIGHT),
                'vx': random.uniform(-120, 120),
                'vy': random.uniform(-400, -100),
                'size': random.uniform(4, 12),
                'color': (random.randint(120,255), random.randint(120,255), random.randint(120,255)),
                'life': random.uniform(1.0, 2.5)
            })
        # shake timer
        self._screen_shake = 0.8
        # show wallpaper9 as victory background if available
        try:
            wp = assets.get_image('wallpaper9.png') or assets.get_image('assets/images/wallpaper9.png')
            if not wp:
                wp = assets.load_image('assets/images/wallpaper9.png')
            if wp:
                self.wallpaper = wp
                self._wallpaper_scaled = None
        except Exception:
            pass

    def show_game_over(self):
        """Chamada quando o jogador perde."""
        self.game_over = True 
        self.game_over_timer = 5.0  # 5 segundos de tela de game over
        
        # Reseta o estado do jogo para começar do início
        self.level_index = 0
        self.score = 0
        self.corrupcao = S.CORRUPCAO_INICIAL
        self.enemies = []
        self.target_enemy = None
        self.current_input = ""
        self.spawn_t = 0.0
        self.boss = None
        self.victory = False

    def update_logic(self, dt):
        if self.victory:
            self.victory_timer -= dt
            # atualiza partículas
            if hasattr(self, 'victory_particles'):
                for p in list(self.victory_particles):
                    p['vy'] += 800 * dt  # gravidade
                    p['x'] += p['vx'] * dt
                    p['y'] += p['vy'] * dt
                    p['life'] -= dt
                    if p['life'] <= 0 or p['y'] > S.HEIGHT + 50:
                        self.victory_particles.remove(p)
            # redução do screen shake
            if getattr(self, '_screen_shake', 0) > 0:
                self._screen_shake = max(0.0, self._screen_shake - dt*1.2)

            if self.victory_timer <= 0:
                self.credits.start()
                self.state = 'credits'
                return
        if self.game_over:
            self.game_over_timer -= dt
            if self.game_over_timer <= 0:
                self.state = 'menu'  # Retorna ao menu
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
            # if self.target_enemy and self.current_input:
            #     if not self.target_enemy.starts_with(self.current_input):
            #         self.current_input = ""
            #         self.target_enemy.matched = 0
            #         self.target_enemy = None
            if self.target_enemy and self.current_input:
                if not self.target_enemy.starts_with(self.current_input):
                # não zera o input, apenas desassocia o inimigo
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
            self.show_game_over()

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
            t = f.render("GAME OVER! Tente novamente.", True, S.COLOR_TEXT_ERROR)
            r = t.get_rect(center=(S.WIDTH // 2, S.HEIGHT // 2))
            self.screen.blit(t, r)
        if self.victory:
            # banner central animado
            f = pygame.font.Font(None, int(48 * S.SCALE))
            t = f.render("MISSAO CUMPRIDA! REDE RESTAURADA.", True, (20, 40, 20))
            # glow/back
            rect = t.get_rect(center=(S.WIDTH // 2, int(S.HEIGHT * 0.45)))
            # desenha glow grande
            glow = pygame.Surface((rect.width+80, rect.height+40), pygame.SRCALPHA)
            for i in range(6,0,-1):
                alpha = int(40 * (i/6))
                pygame.draw.rect(glow, (200,255,200,alpha), glow.get_rect(), border_radius=20)
            g_rect = glow.get_rect(center=rect.center)
            self.screen.blit(glow, g_rect)
            self.screen.blit(t, rect)

            # partículas de vitória
            if hasattr(self, 'victory_particles'):
                for p in self.victory_particles:
                    s = pygame.Surface((int(p['size']), int(p['size'])), pygame.SRCALPHA)
                    pygame.draw.circle(s, (*p['color'], 220), (int(p['size']//2), int(p['size']//2)), int(p['size']//2))
                    self.screen.blit(s, (p['x'], p['y']))

            # leve screen shake deslocando HUD (visual apenas)
            if getattr(self, '_screen_shake', 0) > 0:
                import math, random
                sx = int((random.random()-0.5)*8*self._screen_shake)
                sy = int((random.random()-0.5)*8*self._screen_shake)
                # aplica deslocamento simples no topo (pode ser melhorado)
                pygame.display.get_surface().scroll(dx=sx, dy=sy)

    def _handle_game_input(self, ev):
        """Handle a pygame.KEYDOWN event while in the playing state.
        Updates `self.current_input`, adjusts `target_enemy.matched` and delegates
        to `handle_key_char` for normal character handling.
        """
        try:
            # BACKSPACE: remove last char and update matched state
            if ev.key == pygame.K_BACKSPACE:
                if self.current_input:
                    self.current_input = self.current_input[:-1]
                # recompute matched for target enemy if present
                if self.target_enemy:
                    if self.current_input and self.target_enemy.starts_with(self.current_input):
                        m = 0
                        for a, b in zip(self.target_enemy.word, self.current_input):
                            if a == b:
                                m += 1
                            else:
                                break
                        self.target_enemy.matched = m
                    else:
                        # if no input left or no longer matches, reset matched/target
                        self.target_enemy.matched = 0
                        if not self.current_input:
                            self.target_enemy = None
                return

            # Character input: use ev.unicode when available
            ch = getattr(ev, 'unicode', None)
            if ch and ch.isprintable():
                # normalize to lower-case to match word lists (words are typically lower-case)
                ch = ch.lower()
                # --- filtro: aceita apenas letras que aparecem na palavra alvo atual ---
                try:
                    allowed_chars = set()
                    # se houver um inimigo alvo, só permite letras daquela palavra
                    if self.target_enemy:
                        allowed_chars = set(self.target_enemy.word)
                    else:
                        # se houver boss ativo e sem alvo, permite letras da palavra corrente do boss
                        if (self.boss and not self.boss.defeated) and (getattr(self.boss, 'current', None)):
                            allowed_chars = set(self.boss.current)
                        else:
                            # caso padrão: permite letras que aparecem em qualquer inimigo na tela
                            allowed_chars = set(''.join(e.word for e in self.enemies))
                    # normalize allowed chars to lower-case
                    allowed_chars = set(c.lower() for c in allowed_chars if isinstance(c, str))
                except Exception:
                    allowed_chars = set()

                # se não está nas permitidas, ignora o input (pode tocar som de erro opcionalmente)
                if allowed_chars and ch not in allowed_chars:
                    try:
                        assets.play('error')
                    except Exception:
                        pass
                    return

                # --- novo filtro: só permite formar prefixes válidos de palavras existentes ---
                try:
                    proposed = (self.current_input or "") + ch
                    prefix_ok = False
                    if self.target_enemy:
                        # se existe um alvo, o input precisa ser prefixo da palavra desse alvo
                        prefix_ok = self.target_enemy.starts_with(proposed)
                    else:
                        # sem alvo: permite se for prefixo de qualquer inimigo na tela
                        any_enemy_prefix = any(e.starts_with(proposed) for e in self.enemies)
                        # se boss ativo, também permite prefixo da palavra corrente do boss
                        boss_prefix = False
                        if (self.boss and not self.boss.defeated) and getattr(self.boss, 'current', None):
                            boss_prefix = self.boss.current.startswith(proposed)
                        prefix_ok = any_enemy_prefix or boss_prefix
                except Exception:
                    prefix_ok = True

                if not prefix_ok:
                    try:
                        assets.play('error')
                    except Exception:
                        pass
                    return

                # delegate core logic (this will append to current_input and handle boss logic)
                self.handle_key_char(ch)

                # update matched length for targeted enemy (if any)
                if self.target_enemy:
                    if self.target_enemy.starts_with(self.current_input):
                        m = 0
                        for a, b in zip(self.target_enemy.word, self.current_input):
                            if a == b:
                                m += 1
                            else:
                                break
                        self.target_enemy.matched = m
                    else:
                        # mismatch — clear target and matched
                        self.target_enemy.matched = 0
                        self.target_enemy = None
        except Exception:
            # swallow to avoid crashing the game loop on minor input bugs
            pass

    def run(self):
        elapsed = 0.0
        running = True
        while running:
            dt = self.clock.tick(S.FPS) / 1000.0
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    running = False
                elif ev.type == pygame.VIDEORESIZE:
                    if not self.is_fullscreen:
                        self.last_window_size = (ev.w, ev.h)
                        self.screen = self.create_window(self.last_window_size, fullscreen=False)
                elif ev.type == KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        if self.state == 'menu':
                            running = False
                        elif self.state == 'cutscene':
                            self.cutscene.finish()
                        elif self.state == 'credits':
                            self.credits.finish()
                        else:
                            running = False
                    elif ev.key == pygame.K_F11:
                        # toggles fullscreen como já implementado...
                        pass
                    else:
                        if self.state == 'menu':
                            self.menu.handle_event(ev)
                        elif self.state == 'cutscene':
                            self.cutscene.handle_event(ev)
                        elif self.state == 'credits':
                            self.credits.handle_event(ev)
                        else:
                            # input do jogador no jogo
                            self._handle_game_input(ev)

            # updates por estado
            if self.state == 'playing':
                self.update_logic(dt)
            elif self.state == 'cutscene':
                self.cutscene.update(dt)
            elif self.state == 'credits':
                self.credits.update(dt)

            # desenho por estado — IMPORTANTE: não desenha o jogo quando em credits
            if self.state == 'menu':
                self.menu.draw(self.screen)
            elif self.state == 'cutscene':
                self.cutscene.draw(self.screen)
            elif self.state == 'credits':
                # desenha apenas os créditos (tela preta + textos)
                self.credits.draw(self.screen)
            else:  # playing / victory / game_over
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
