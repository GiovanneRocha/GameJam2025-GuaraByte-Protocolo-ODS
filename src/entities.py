# -*- coding: utf-8 -*-
import random
import pygame
import settings as S
from utils import clamp, draw_label_box, make_font

class WordEnemy:
    def __init__(self, words, speed_factor=1.0):
        self.word = random.choice(words)
        # Start somewhere near top
        self.x = random.randint(int(24*S.SCALE), S.WIDTH - int(24*S.SCALE))
        self.y = random.randint(int(-180*S.SCALE), int(-80*S.SCALE))
        vy_min, vy_max = S.ENEMY_VY_RANGE
        vx_min, vx_max = S.ENEMY_VX_RANGE
        self.vy = random.uniform(vy_min, vy_max) * speed_factor
        self.vx = random.uniform(vx_min, vx_max) * speed_factor
        self.matched = 0

    def starts_with(self, prefix: str) -> bool:
        return self.word.startswith(prefix)

    def consume_char(self, ch: str) -> bool:
        if self.matched < len(self.word) and ch == self.word[self.matched]:
            self.matched += 1
            return True
        return False

    def is_completed(self) -> bool:
        return self.matched >= len(self.word)

    def is_off_bottom(self) -> bool:
        return self.y - int(20*S.SCALE) > S.HEIGHT

    def update(self, dt):
        # Move and bounce on side walls
        self.x += self.vx * dt
        self.y += self.vy * dt
        margin = int(S.MARGIN_X * S.SCALE)
        # Fit a provisional width estimate to keep horizontally inside
        # If touches side walls, bounce
        if self.x < margin:
            self.x = margin
            self.vx = abs(self.vx)
        if self.x > S.WIDTH - margin:
            self.x = S.WIDTH - margin
            self.vx = -abs(self.vx)

    def draw(self, screen):
        # Box max width: leave side margins
        max_w = S.WIDTH - int(32*S.SCALE)
        done = self.word[:self.matched]
        todo = self.word[self.matched:]
        rect, total_w, font = draw_label_box(screen, done, todo, (int(self.x), int(self.y)), max_w)
        # Progress bar
        prog_w = int(total_w * (self.matched / max(1, len(self.word))))
        if prog_w > 0:
            bar_rect = pygame.Rect(rect.x + int(12*S.SCALE), rect.bottom - int(8*S.SCALE), prog_w, int(6*S.SCALE))
            pygame.draw.rect(screen, (80,220,140), bar_rect, border_radius=int(3*S.SCALE))


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
