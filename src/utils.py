
# -*- coding: utf-8 -*-
import pygame
import settings as S


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def draw_grid_background(screen, bg_color, grid_color):
    screen.fill(bg_color)
    step = int(48 * S.SCALE)
    step = max(32, step)
    w, h = S.WIDTH, S.HEIGHT
    for x in range(0, w, step):
        pygame.draw.line(screen, grid_color, (x, 0), (x, h))
    for y in range(0, h, step):
        pygame.draw.line(screen, grid_color, (0, y), (w, y))


def make_font(px, bold=False):
    size = max(10, int(px * S.SCALE))
    try:
        return pygame.font.SysFont("Consolas", size, bold=bold)
    except Exception:
        return pygame.font.Font(None, size)


def fit_font_for_text(text: str, max_width: int, max_px: int, min_px: int = 10, bold=False):
    """Find the largest font size in [min_px, max_px] that makes text <= max_width."""
    lo, hi = min_px, max_px
    best_font = make_font(min_px, bold)
    best_w = best_font.size(text)[0]
    while lo <= hi:
        mid = (lo + hi) // 2
        f = make_font(mid, bold)
        w, _ = f.size(text)
        if w <= max_width:
            best_font, best_w = f, w
            lo = mid + 1
        else:
            hi = mid - 1
    return best_font


def draw_label_box(screen, text_done, text_todo, center_pos, max_width_px):
    """Draws a rounded box containing text (done+todo) fitted to max width."""
    full_text = text_done + text_todo
    pad_x = int(12 * S.SCALE)
    pad_y = int(8 * S.SCALE)
    font = fit_font_for_text(full_text, max(60, max_width_px - pad_x*2), int(32 * S.SCALE), 10)
    done_s = font.render(text_done, True, (120,255,160))
    todo_s = font.render(text_todo, True, S.COLOR_TEXT_DEFAULT)
    tw = done_s.get_width() + todo_s.get_width()
    th = max(done_s.get_height(), todo_s.get_height())

    rect_w = tw + pad_x*2
    rect_h = th + pad_y*2
    cx, cy = center_pos
    rect_x = int(cx - rect_w/2)
    rect_y = int(cy - rect_h/2)
    # Keep fully inside the screen horizontally
    rect_x = clamp(rect_x, int(8*S.SCALE), S.WIDTH - rect_w - int(8*S.SCALE))
    pygame.draw.rect(screen, (40,35,50), (rect_x, rect_y, rect_w, rect_h), border_radius=int(10*S.SCALE))

    # Progress bar
    total_w = rect_w - pad_x*2
    # draw after word consumer sets matched length outside

    # Draw text centered inside rect
    tx = rect_x + pad_x + (total_w - tw)//2
    ty = rect_y + pad_y
    screen.blit(done_s, (tx, ty))
    screen.blit(todo_s, (tx + done_s.get_width(), ty))

    return pygame.Rect(rect_x, rect_y, rect_w, rect_h), total_w, font
