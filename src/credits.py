import pygame
import settings as S
import assets

class Credits:
    def __init__(self, game):
        self.game = game
        self.running = False
        # velocidade mais lenta, cinematográfica (~30 px/s)
        self.scroll_speed = 90  # pixels por second (filme-like)
        self.scroll_y = 0

        # Lista de créditos (ajuste conforme necessário)
        self.credits_text = [
            ("GuaraByte: Protocolo ODS", 48),
            ("", 20),
            ("Desenvolvimento", 36),
            ("Equipe GuaraByte", 24),
            ("", 20),
            ("Programação", 36),
            ("Nome do Programador 1", 24),
            ("Nome do Programador 2", 24),
            ("", 20),
            ("Arte", 36),
            ("Nome do Artista 1", 24),
            ("Nome do Artista 2", 24),
            ("", 20),
            ("Música & Som", 36),
            ("Nome do Músico", 24),
            ("", 20),
            ("Agradecimentos Especiais", 36),
            ("Nome 1", 24),
            ("Nome 2", 24),
            ("", 20),
            ("Feito com Pygame", 36),
            ("2024", 24),
        ]

        self.rendered_lines = []
        total_h = 0
        spacing = int(40 * getattr(S, 'SCALE', 1.0))
        for text, size in self.credits_text:
            font = pygame.font.Font(None, int(size * getattr(S, 'SCALE', 1.0)))
            surf = font.render(text, True, getattr(S, 'COLOR_TEXT', (220,220,220)))
            self.rendered_lines.append((surf, surf.get_height()))
            total_h += surf.get_height() + spacing
        self.total_height = total_h

    def start(self):
        self.running = True
        # começa abaixo da tela
        self.scroll_y = S.HEIGHT + 30
        # toca música de créditos (assets/musics/credits.mp3)
        try:
            assets.play_music('musics/credits.mp3', getattr(S, 'MUSIC_VOLUME', 0.6))
        except Exception:
            try:
                assets.play_music('credits.mp3', getattr(S, 'MUSIC_VOLUME', 0.6))
            except Exception:
                pass

    def finish(self):
        self.running = False
        # para música dos créditos
        try:
            assets.stop_music()
        except Exception:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
        self.game.state = 'menu'

    def handle_event(self, ev):
        if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_SPACE):
            self.finish()

    def update(self, dt):
        if not self.running:
            return
        # sobe devagar (film-like)
        self.scroll_y -= self.scroll_speed * dt
        # quando terminar, volta ao menu automaticamente
        if self.scroll_y < -self.total_height - 50:
            self.finish()

    def draw(self, screen):
        # fundo totalmente preto (sem nenhum outro elemento por trás)
        screen.fill((0, 0, 0))

        # desenha apenas as linhas de texto, uma por vez, sem imagens por trás
        y = self.scroll_y
        spacing = int(40 * getattr(S, 'SCALE', 1.0))
        for surf, h in self.rendered_lines:
            r = surf.get_rect(centerx=S.WIDTH//2)
            r.top = int(y)
            screen.blit(surf, r)
            y += h + spacing