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
            ("GuaráByte: Protocolo ODS", 48),
            ("", 40),
            ("Uma Produção da Equipe", 36),
            ("GuaráByte", 30),
            ("", 40),
            ("Desenvolvimento e Programação", 36),
            ("Giovanne Rocha Vieira", 28),
            ("Gabriel Henrique de Sena", 28),
            ("Danilo Vicentin", 28),
            ("João Paulo Duarte Pimentel", 28),
            ("", 40),
            ("Arte, Vídeo e Animação (IA)", 36),
            ("Pippit", 28),
            ("PixVerse", 28),
            ("", 40),
            ("Música & Efeitos Sonoros", 36),
            ("Pixabay", 28),
            ("", 40),
            ("Ferramentas Auxiliares (IA)", 36),
            ("Git Copilot", 28),
            ("Gemini Pro", 28),
            ("", 40),
            ("Agradecimentos Especiais", 36),
            ("Organização da Game Jam", 28),
            ("Professores da FATEC Campinas", 28),
            ("", 60),
            ("Feito com Pygame", 36),
            ("", 20),
            ("Game Jam FATEC Campinas 2025", 28),
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