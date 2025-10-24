# -*- coding: utf-8 -*-
import os
import pygame

# pasta 'assets' está uma pasta acima de src
ASSETS_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets'))
IMG_DIR = os.path.join(ASSETS_ROOT, 'img')
SFX_DIR = os.path.join(ASSETS_ROOT, 'sfx')
MUSIC_DIR = os.path.join(ASSETS_ROOT, 'music')

_images = {}
_sfx = {}
_current_music = None


def load_assets():
    """Carrega efeitos sonoros."""
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    # preload sfx
    if os.path.isdir(SFX_DIR):
        for fn in os.listdir(SFX_DIR):
            full = os.path.join(SFX_DIR, fn)
            if os.path.isfile(full):
                name, ext = os.path.splitext(fn)
                try:
                    _sfx[name] = pygame.mixer.Sound(full)
                except Exception:
                    pass


def get_image(path: str) -> pygame.Surface:
    """Carrega e cacheia uma imagem."""
    if not path:
        return None

    if path in _images:
        return _images[path]

    # Tenta diferentes caminhos
    try_paths = [
        path,  # caminho absoluto
        os.path.join(IMG_DIR, path),  # em assets/img
        os.path.join(ASSETS_ROOT, path),  # em assets/
        os.path.join(IMG_DIR, os.path.basename(path))  # apenas nome do arquivo em img/
    ]

    for try_path in try_paths:
        if os.path.exists(try_path):
            try:
                img = pygame.image.load(try_path)
                surf = img.convert_alpha() if img.get_alpha() else img.convert()
                _images[path] = surf
                return surf
            except Exception:
                continue

    return None


def play_music(path: str, volume: float = 0.6):
    """Toca música em loop."""
    global _current_music

    if not path:
        return False

    # Se já está tocando esta música, apenas ajusta volume
    if path == _current_music:
        pygame.mixer.music.set_volume(volume)
        return True

    # Tenta diferentes caminhos
    try_paths = [
        path,  # caminho absoluto
        os.path.join(MUSIC_DIR, path),  # em assets/music
        os.path.join(ASSETS_ROOT, path),  # em assets/
        os.path.join(MUSIC_DIR, os.path.basename(path))  # apenas nome em music/
    ]

    for try_path in try_paths:
        if os.path.exists(try_path):
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(try_path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)  # -1 = loop infinito
                _current_music = path
                return True
            except Exception:
                continue

    return False


def stop_music():
    """Para a música atual."""
    global _current_music
    try:
        pygame.mixer.music.stop()
        _current_music = None
    except Exception:
        pass


def play(sfx_name: str, volume: float = 1.0):
    """Toca um efeito sonoro."""
    if sfx_name in _sfx:
        _sfx[sfx_name].set_volume(volume)
        _sfx[sfx_name].play()
