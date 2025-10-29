import os
import pygame
from pygame.locals import KEYDOWN
import settings as S
import assets

class Menu:
    def __init__(self, game):
        self.game = game
        self.options = ["Jogar", "Créditos", "Sair"]
        self.selected = 0

        # tenta carregar wallpaper e título via assets
        self.wallpaper = None
        self.title_img = None
        try:
            self.wallpaper = assets.get_image('images/wallpaper_menu.png') or assets.get_image('wallpaper_menu.png')
        except Exception:
            self.wallpaper = None
        try:
            self.title_img = assets.get_image('images/titulo.png') or assets.get_image('titulo.png')
        except Exception:
            self.title_img = None

        # música do menu (não crítica)
        try:
            assets.play_music('menu.mp3', getattr(S, 'MUSIC_VOLUME', 0.6))
        except Exception:
            pass

    def handle_event(self, ev):
        if ev.type != pygame.KEYDOWN:
            return
        if ev.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.options)
        elif ev.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.options)
        elif ev.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            choice = self.options[self.selected]
            if choice == "Jogar":
                # Reseta flags importantes
                self.game.game_over = False
                self.game.victory = False
                
                # Verifica se deve mostrar cutscene apenas na primeira vez
                if not hasattr(self, '_showed_cutscene'):
                    if self.game.cutscene.has_video():
                        self.game.cutscene.start()
                        self.game.state = 'cutscene'
                        self._showed_cutscene = True
                        return
                
                # Se já mostrou cutscene ou não tem, vai direto para o jogo
                self.game.begin_level(self.game.level_index)
                self.game.state = 'playing'
                
            elif choice == "Créditos":
                self.game.credits.start()
                self.game.state = 'credits'
            elif choice == "Sair":
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self, screen):
        # fundo: wallpaper se tiver, senão cor sólida
        if self.wallpaper:
            try:
                img = pygame.transform.smoothscale(self.wallpaper, (S.WIDTH, S.HEIGHT))
            except Exception:
                img = pygame.transform.scale(self.wallpaper, (S.WIDTH, S.HEIGHT))
            screen.blit(img, (0, 0))
        else:
            screen.fill((12, 16, 30))

        # título: imagem centralizada mais próxima do meio
        if self.title_img:
            ti_w = int(S.WIDTH * 0.5)  
            try:
                tit_surf = pygame.transform.smoothscale(self.title_img, (ti_w, int(ti_w * (self.title_img.get_height()/max(1,self.title_img.get_width())))))
            except Exception:
                tit_surf = pygame.transform.scale(self.title_img, (ti_w, int(ti_w * (self.title_img.get_height()/max(1,self.title_img.get_width())))))
            # Posiciona mais próximo do meio
            tr = tit_surf.get_rect(center=(S.WIDTH//2, int(S.HEIGHT * 0.3)))
            screen.blit(tit_surf, tr)
        else:
            f_title = pygame.font.Font(None, int(64 * getattr(S, 'SCALE', 1.0)))
            t = f_title.render(S.TITLE, True, getattr(S, 'COLOR_TEXT', (220,220,220)))
            r = t.get_rect(center=(S.WIDTH//2, int(S.HEIGHT * 0.3)))
            screen.blit(t, r)

        # menu options: botões mais abaixo
        f = pygame.font.Font(None, int(34 * getattr(S, 'SCALE', 1.0)))
        btn_w = int(S.WIDTH * 0.4)
        btn_h = int(56 * getattr(S, 'SCALE', 1.0))
        start_y = int(S.HEIGHT * 0.6)  # Descido para 60% da altura
        for i, opt in enumerate(self.options):
            x = (S.WIDTH - btn_w) // 2
            y = start_y + i * (btn_h + int(16 * getattr(S, 'SCALE', 1.0)))
            # botão
            if i == self.selected:
                bg = (220, 200, 80)
                fg = (20, 18, 24)
                outline = (255, 235, 140)
            else:
                bg = (30, 30, 40, )
                fg = getattr(S, 'COLOR_TEXT', (220,220,220))
                outline = (0,0,0)
            rect = pygame.Rect(x, y, btn_w, btn_h)
            # fundo do botão com leve transparência (se surface com alpha)
            s = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
            s.fill((*bg[:3], 220))
            screen.blit(s, (x, y))
            # texto
            txt = f.render(opt, True, fg)
            tr = txt.get_rect(center=rect.center)
            screen.blit(txt, tr)
            # contorno sutil
            pygame.draw.rect(screen, outline, rect, 2)