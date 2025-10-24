# -*- coding: utf-8 -*-
import os
import pygame

# pasta 'assets' está uma pasta acima de src
ASSETS_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets'))
# Pastas dentro de assets - use exatamente as pastas que você tem: images, sounds, musics
IMAGES_DIR = os.path.join(ASSETS_ROOT, 'images')
SOUNDS_DIR = os.path.join(ASSETS_ROOT, 'sounds')
MUSICS_DIR = os.path.join(ASSETS_ROOT, 'musics')

# Dicionários para armazenar assets
_images = {}
_sounds = {}
_current_music = None


def get_asset_path(folder_dir, filename):
    if not filename:
        return None
    # absoluto direto
    if os.path.isabs(filename) and os.path.exists(filename):
        return filename

    # aceitar strings que já contenham "assets/..." ou "assets\..."
    fn = filename.replace('\\', '/')
    if fn.startswith('assets/'):
        rel = fn[len('assets/'):].lstrip('/\\')
        candidate = os.path.join(ASSETS_ROOT, rel)
        if os.path.exists(candidate):
            return candidate

    # se for nome simples (ex: 'wallpaper4.png'), tenta na pasta específica
    path = os.path.join(folder_dir, filename)
    if os.path.exists(path):
        return path

    # tenta direto em ASSETS_ROOT (ex: filename = 'images/wallpaper4.png' ou 'wallpaper4.png')
    alt = os.path.join(ASSETS_ROOT, filename)
    if os.path.exists(alt):
        return alt

    # tenta relativo ao projeto (caso filename seja relativo a outro lugar)
    proj_root = os.path.dirname(os.path.dirname(__file__))
    alt2 = os.path.join(proj_root, filename)
    if os.path.exists(alt2):
        return alt2

    return None


def load_assets():
    global _images, _sounds

    # lista de imagens esperadas (chave -> arquivo)
    image_files = {
        'guara': 'guara.png',
        'virus': 'virus.png',
        'background': 'background.png'
    }

    for key, filename in image_files.items():
        try:
            path = get_asset_path(IMAGES_DIR, filename)
            if path:
                _images[key] = pygame.image.load(path).convert_alpha()
            else:
                print(f"[assets] imagem não encontrada: {filename}")
                _images[key] = None
        except Exception as e:
            print(f"[assets] Erro ao carregar imagem {filename}: {e}")
            _images[key] = None

    # lista de sons esperados (chave -> arquivo)
    sound_files = {
        'ok': 'type_ok.wav',
        'clean': 'word_clean.wav'
    }

    for key, filename in sound_files.items():
        try:
            path = get_asset_path(SOUNDS_DIR, filename)
            if path:
                _sounds[key] = pygame.mixer.Sound(path)
            else:
                print(f"[assets] som não encontrado: {filename}")
                _sounds[key] = None
        except Exception as e:
            print(f"[assets] Erro ao carregar som {filename}: {e}")
            _sounds[key] = None


def load_image(filename):
    """Carrega e retorna uma Surface para um arquivo de imagem (caminho, nome simples ou 'assets/..')."""
    if not filename:
        return None
    path = get_asset_path(IMAGES_DIR, filename)
    if not path:
        return None
    try:
        surf = pygame.image.load(path).convert_alpha()
        # cache usando o nome do arquivo para facilitar reuso
        key = os.path.basename(path)
        _images[key] = surf
        return surf
    except Exception as e:
        print(f"[assets] Erro ao carregar imagem (load_image) {filename}: {e}")
        return None


def play(sound_name):
    if sound_name in _sounds and _sounds[sound_name]:
        try:
            _sounds[sound_name].play()
        except Exception as e:
            print(f"[assets] Erro ao tocar som {sound_name}: {e}")


def stop_music():
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass


def play_music(filename, volume=0.6):
    """
    filename pode ser:
      - nome do arquivo presente em assets/musics (ex: 'back_music1.mp3')
      - caminho relativo com prefixo 'assets/...' (ex: 'assets/musics/back_music1.mp3')
      - caminho absoluto existente
    """
    global _current_music
    if not filename:
        return False
    try:
        path = get_asset_path(MUSICS_DIR, filename)
        if not path:
            print(f"[assets] música não encontrada: {filename}")
            return False
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)  # loop infinito
        _current_music = path
        return True
    except Exception as e:
        print(f"[assets] Erro ao carregar/tocar música {filename}: {e}")
        return False


def get_image(name):
    """
    Retorna uma Surface a partir de:
      - chave carregada em _images (ex: 'guara', 'virus', 'background')
      - nome de arquivo já carregado e cacheado (ex: 'wallpaper4.png')
      - tenta carregar dinamicamente se passado um caminho/nome
    """
    if not name:
        return None
    # chave direta
    if name in _images:
        return _images[name]
    # basename se o usuário passou algo como 'assets/images/wallpaper4.png' ou 'images/wallpaper4.png'
    base = os.path.basename(name)
    if base in _images:
        return _images[base]
    # tenta carregar dinamicamente (aceita 'assets/...' ou nome simples)
    img = load_image(name)
    if img:
        return img
    return None
