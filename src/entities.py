# -*- coding: utf-8 -*-
import random
import pygame
import settings as S
import assets

class WordEnemy:
    def __init__(self, words, x=0, y=0, speed: float = 0.0, speed_factor: float = 1.0):
        """
        words: lista de palavras possíveis ou única palavra conforme implementação do projeto
        speed: velocidade base
        speed_factor: multiplicador (aceita chamada com speed_factor=...)
        """
        # aceita tanto lista de palavras quanto string
        if isinstance(words, (list, tuple)):
            self.word = random.choice(words)
        else:
            self.word = str(words)

        self.x = x if x else random.uniform(50, S.WIDTH - 50)
        self.y = y if y else -30.0
        # aplica fator de velocidade
        self.speed = (speed or S.DEFAULT_ENEMY_SPEED) * float(speed_factor)

        # estados de digitação / correspondência
        self.matched = 0
        self.dead = False

        # randomiza imagem entre virus1..virus4.png (procura em assets/images)
        self.image = None
        try:
            idx = random.randint(1, 4)
            img = None
            # tenta caminhos comuns que o módulo assets possa esperar
            for p in (f'images/virus{idx}.png', f'virus{idx}.png'):
                try:
                    img = assets.get_image(p)
                    if img:
                        break
                except Exception:
                    img = None
            if img:
                self.image = img
        except Exception:
            self.image = None

    def starts_with(self, prefix: str) -> bool:
        return self.word.startswith(prefix)

    def update(self, dt: float):
        self.y += self.speed * dt

    def is_off_bottom(self) -> bool:
        return self.y > S.HEIGHT + 50

    def draw(self, surface):
        # primeiro desenha o texto (base) — assim a imagem pode ficar por cima
        try:
            font = pygame.font.Font(None, int(20 * getattr(S, 'SCALE', 1.0)))
            txt = self.word
            txt_surf = font.render(txt, True, getattr(S, 'COLOR_TEXT', (220,220,220)))
            # posiciona texto logo abaixo do vírus (ajuste conforme preferir)
            txt_rect = txt_surf.get_rect(center=(int(self.x), int(self.y + 28)))
            surface.blit(txt_surf, txt_rect)
        except Exception:
            pass

        # depois desenha a imagem do vírus por cima do texto
        if self.image:
            try:
                w = int(48 * getattr(S, 'SCALE', 1.0))
                h = int(48 * getattr(S, 'SCALE', 1.0))
                img = pygame.transform.smoothscale(self.image, (w, h))
            except Exception:
                img = pygame.transform.scale(self.image, (w, h))
            surface.blit(img, (int(self.x - w//2), int(self.y - h//2)))
        
        # Box max width: leave side margins
        max_w = S.WIDTH - int(32*S.SCALE)
        done = self.word[:self.matched]
        todo = self.word[self.matched:]
        rect, total_w, font = draw_label_box(surface, done, todo, (int(self.x), int(self.y)), max_w)
        # Progress bar
        prog_w = int(total_w * (self.matched / max(1, len(self.word))))
        if prog_w > 0:
            bar_rect = pygame.Rect(rect.x + int(12*S.SCALE), rect.bottom - int(8*S.SCALE), prog_w, int(6*S.SCALE))
            pygame.draw.rect(surface, (80,220,140), bar_rect, border_radius=int(3*S.SCALE))


class Boss:
    def __init__(self, words: list[str], health: int):
        ws = list(words)
        random.shuffle(ws)
        self.queue = ws
        self.health = health
        self.current = self.queue.pop(0) if self.queue else ""
        self.matched = 0
        self.spawn_t = 0.0
        self.spawn_interval = 1.8  # seconds
        self.defeated = False

    def handle_char(self, ch) -> tuple[bool, bool, str | None]:
        """
        Retorna (ok, completed, completed_word_or_None).
        ok: caractere aceito (bateu com o próximo expected)
        completed: palavra do boss foi totalmente digitada
        completed_word_or_None: a palavra que foi completada (antes de trocar para a próxima)
        """
        if self.defeated or not self.current:
            return (False, False, None)
        if self.matched < len(self.current) and ch == self.current[self.matched]:
            self.matched += 1
            if self.matched == len(self.current):
                completed_word = self.current
                self.health -= 1
                if self.health <= 0:
                    self.defeated = True
                    self.current = ""
                    self.matched = 0
                else:
                    self.current = self.queue.pop(0) if self.queue else ""
                    self.matched = 0
                return (True, True, completed_word)
            return (True, False, None)
        return (False, False, None)

    def update(self, dt):
        self.spawn_t += dt

    def should_spawn_minion(self) -> bool:
        return (not self.defeated) and (self.spawn_t >= self.spawn_interval)

    def reset_spawn(self):
        self.spawn_t = 0.0

    def clear_current(self):
        """Limpa a palavra corrente do boss (usado quando jogador completa/remover)"""
        try:
            if hasattr(self, 'current'):
                self.current = ""
            if hasattr(self, 'matched'):
                self.matched = 0
        except Exception:
            pass
