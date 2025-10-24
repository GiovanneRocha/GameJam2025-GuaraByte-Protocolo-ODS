
# -*- coding: utf-8 -*-
import pygame
import settings as S
from utils import make_font, clamp


def draw_hud(screen, cfg, score, corrupcao):
    pad = int(10*S.SCALE)
    hud_h = int(92*S.SCALE)
    pygame.draw.rect(screen, S.COLOR_PANEL_BG, (0, 0, S.WIDTH, hud_h))
    title_f = make_font(26, True)
    sub_f   = make_font(16, False)
    t1 = title_f.render(cfg.name, True, (220,230,255))
    t2 = sub_f.render(cfg.ods, True, (190,200,230))
    screen.blit(t1, (pad, pad))
    screen.blit(t2, (pad, pad + t1.get_height() + int(4*S.SCALE)))

    scr_f = make_font(22, True)
    scr = scr_f.render(f"Score: {score}", True, (255,255,255))
    screen.blit(scr, (S.WIDTH - scr.get_width() - pad, pad))

    # Corrupcao bar
    bar_w = S.WIDTH - pad*2
    bar_x = pad
    bar_y = hud_h - int(22*S.SCALE)
    pygame.draw.rect(screen, (50,40,55), (bar_x, bar_y, bar_w, int(12*S.SCALE)), border_radius=int(6*S.SCALE))
    wfill = int(bar_w * max(0, min(1, corrupcao/100.0)))
    col = (240,110,110) if corrupcao < 35 else (255,210,80) if corrupcao < 65 else (120,230,160)
    pygame.draw.rect(screen, col, (bar_x, bar_y, wfill, int(12*S.SCALE)), border_radius=int(6*S.SCALE))

    return hud_h


def draw_boss_banner(screen, boss, top_y):
    if not boss or boss.defeated:
        return top_y
    bw = int(S.WIDTH * 0.92)
    bh = int(74*S.SCALE)
    bx = (S.WIDTH - bw)//2
    by = top_y + int(8*S.SCALE)
    pygame.draw.rect(screen, (50,24,40), (bx, by, bw, bh), border_radius=int(12*S.SCALE))

    sub_f   = make_font(16)
    hp_txt = sub_f.render(f"Boss HP: {boss.health}", True, (255,190,210))
    screen.blit(hp_txt, (bx + int(12*S.SCALE), by + int(8*S.SCALE)))

    # Fit boss word inside banner
    word = boss.current
    # try a font that fits ~bw - padding
    avail = bw - int(24*S.SCALE)
    # progressively reduce font until fits
    size = int(32*S.SCALE)
    while size >= int(14*S.SCALE):
        f = make_font(size, True)
        w, h = f.size(word)
        if w <= avail:
            done = f.render(word[:boss.matched], True, (255,140,170))
            todo = f.render(word[boss.matched:], True, (250,230,240))
            tx = bx + (bw - (done.get_width()+todo.get_width()))//2
            ty = by + bh//2 - done.get_height()//2 + int(6*S.SCALE)
            screen.blit(done, (tx, ty))
            screen.blit(todo, (tx + done.get_width(), ty))
            break
        size -= 2

    return by + bh


def draw_instructions(screen, current_input):
    panel_h = int(64*S.SCALE)
    y = S.HEIGHT - panel_h
    pygame.draw.rect(screen, S.COLOR_PANEL_BG, (0, y, S.WIDTH, panel_h))
    msg = "Digite para depurar • BACKSPACE apaga • ESC sai • Dica: com Boss ativo, inicie nova palavra para mudar o alvo"
    f = make_font(14)
    t = f.render(msg, True, (210,210,230))
    x = max(8, (S.WIDTH - t.get_width())//2)
    screen.blit(t, (x, y + (panel_h - t.get_height())//2))

    # input do jogador
    pf = make_font(28, True)
    inp = pf.render(current_input, True, S.COLOR_PLAYER_INPUT)
    ir = inp.get_rect(center=(S.WIDTH//2, S.HEIGHT - int(84*S.SCALE)))
    screen.blit(inp, ir)
