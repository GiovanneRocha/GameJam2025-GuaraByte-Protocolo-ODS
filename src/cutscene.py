import os
import sys
import pygame
import tempfile
import subprocess
import shutil
import settings as S
import assets

# tenta imports opcionais
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except Exception:
    CV2_AVAILABLE = False
    print("Aviso: opencv-python não está instalado. Instale com: pip install opencv-python")

# tenta moviepy, mas não falha se não existir
try:
    from moviepy.editor import VideoFileClip
    MOVIEPY_AVAILABLE = True
except Exception:
    VideoFileClip = None
    MOVIEPY_AVAILABLE = False
    # não imprimir stack, só aviso curto
    print("moviepy não disponível: fallback para ffmpeg (se instalado).")

class Cutscene:
    def __init__(self, game, slides=None, slide_time=3.0):
        self.game = game
        self.slide_time = slide_time
        self.current = 0
        self.t = 0.0
        self.running = False

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        candidate = os.path.join(base_dir, 'assets', 'videos', 'Cutscene.mp4')
        self.video_path = candidate if os.path.exists(candidate) else None

        # flags / handles
        self.cap = None
        self._has_video = bool(self.video_path) and CV2_AVAILABLE
        self.video_fps = 30.0
        self.frame_time = 1 / 30.0
        self.next_frame_time = 0.0
        self._last_surface = None

        # audio temp file (extracted from mp4) quando necessário
        self._temp_audio_path = None

        # tenta localizar intro.mp3 em assets/musics
        self.intro_music_path = None
        self.has_intro_music = False
        try:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            possible = os.path.join(base_dir, 'assets', 'musics', 'intro.mp3')
            if os.path.exists(possible):
                self.intro_music_path = possible
                self.has_intro_music = True
            else:
                # tenta via módulo assets (se disponível)
                try:
                    m = assets.get_music('intro.mp3')
                    if m:
                        self.intro_music_path = m
                        self.has_intro_music = True
                except Exception:
                    pass
        except Exception:
            self.has_intro_music = False

        # fallback slides se não houver vídeo
        if slides is None:
            self.slides = [
                "GUARABYTE PROTOCOL - Protocolo ODS",
                "Pressione Enter ou Espaço para pular..."
            ]
        else:
            self.slides = slides if isinstance(slides, (list, tuple)) else [slides]

    def has_slides(self):
        return bool(self.slides) or self._has_video

    def has_video(self):
        return self._has_video

    def _extract_audio_moviepy(self):
        try:
            clip = VideoFileClip(self.video_path)
            # cria temp WAV/MP3
            tf = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tf.close()
            out_path = tf.name
            clip.audio.write_audiofile(out_path, verbose=False, logger=None)
            clip.close()
            return out_path
        except Exception as e:
            # falhou -> cleanup e retorna None
            try:
                if 'out_path' in locals() and os.path.exists(out_path):
                    os.unlink(out_path)
            except Exception:
                pass
            return None

    def _extract_audio_ffmpeg(self):
        ff = shutil.which('ffmpeg') or shutil.which('ffmpeg.exe')
        if not ff:
            return None
        tf = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        tf.close()
        out_path = tf.name
        try:
            # extrai áudio para WAV com ffmpeg
            cmd = [ff, '-y', '-i', self.video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', out_path]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return out_path
        except Exception:
            try:
                if os.path.exists(out_path):
                    os.unlink(out_path)
            except Exception:
                pass
            return None

    def _prepare_audio(self):
        """
        Tenta extrair áudio prioritariamente com ffmpeg (mais fácil de instalar).
        Se ffmpeg não estiver disponível, tenta moviepy se presente.
        Retorna caminho do arquivo de áudio temporário ou None.
        """
        audio_path = None

        # tenta ffmpeg primeiro
        if self.video_path:
            ff = shutil.which('ffmpeg') or shutil.which('ffmpeg.exe')
            if ff:
                audio_path = self._extract_audio_ffmpeg()
                if audio_path:
                    return audio_path

        # se ffmpeg não funcionou, tenta moviepy como fallback
        if MOVIEPY_AVAILABLE and self.video_path:
            audio_path = self._extract_audio_moviepy()
            if audio_path:
                return audio_path

        # nenhum método disponível
        print("Aviso: não foi possível extrair áudio do vídeo (ffmpeg e moviepy não disponíveis). Cutscene sem som.")
        self._temp_audio_path = None
        return None

    def start(self):
        self.current = 0
        self.t = 0.0
        self.running = True
        self.next_frame_time = 0.0
        self._last_surface = None

        # inicia captura de vídeo se disponível
        if self._has_video:
            try:
                import cv2  # reimport seguro
                self.cap = cv2.VideoCapture(self.video_path)
                if self.cap.isOpened():
                    self.video_fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
                    if self.video_fps <= 0:
                        self.video_fps = 30.0
                    self.frame_time = 1.0 / self.video_fps
                    self.next_frame_time = 0.0
                else:
                    try:
                        self.cap.release()
                    except Exception:
                        pass
                    self.cap = None
                    self._has_video = False
            except Exception:
                self.cap = None
                self._has_video = False

        # Para música atual e inicia intro.mp3 (se existir)
        try:
            # assets.stop_music pode não existir; tenta de forma segura
            try:
                assets.stop_music()
            except Exception:
                try:
                    pygame.mixer.music.stop()
                except Exception:
                    pass

            if self.has_intro_music and self.intro_music_path:
                # preferir assets.play_music se disponível
                try:
                    assets.play_music('intro.mp3', getattr(S, 'MUSIC_VOLUME', 0.6))
                except Exception:
                    # fallback para carregar diretamente o arquivo
                    try:
                        pygame.mixer.music.load(self.intro_music_path)
                        pygame.mixer.music.play()
                    except Exception:
                        pass
        except Exception:
            print("Aviso: não foi possível iniciar música de intro para a cutscene.")

    def finish(self):
        # para reprodução e libera recursos
        self.running = False
        try:
            # para a música da intro (independente de como foi tocada)
            try:
                assets.stop_music()
            except Exception:
                try:
                    pygame.mixer.music.stop()
                except Exception:
                    pass
        except Exception:
            pass

        if self.cap:
            try:
                self.cap.release()
            except Exception:
                pass
            self.cap = None

        # remove áudio temporário se foi criado (não usado aqui, mas mantido por segurança)
        if self._temp_audio_path and os.path.exists(self._temp_audio_path):
            try:
                os.unlink(self._temp_audio_path)
            except Exception:
                pass
            self._temp_audio_path = None

        # inicia fase
        try:
            self.game.begin_level(self.game.level_index)
        except Exception:
            pass
        self.game.state = 'playing'
        # reinicia música de fundo do jogo (se houver)
        try:
            assets.play_music('background.mp3', getattr(S, 'MUSIC_VOLUME', 0.6))
        except Exception:
            pass

    def handle_event(self, ev):
        if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            self.finish()

    def update(self, dt):
        if not self.running:
            return
        self.t += dt
        if self._has_video and self.cap:
            # avança frames conforme tempo; apenas lê quando for hora do próximo frame
            if self.t >= self.next_frame_time:
                try:
                    ret, frame = self.cap.read()
                    if not ret:
                        # vídeo acabou
                        self.finish()
                        return
                    # converte BGR->RGB e cria surface (guarda para draw)
                    frame = frame[:, :, ::-1]  # BGR->RGB
                    h, w = frame.shape[:2]
                    surf = pygame.image.frombuffer(frame.tobytes(), (w, h), 'RGB')
                    self._last_surface = surf
                    # agenda próximo frame
                    self.next_frame_time = self.t + self.frame_time
                except Exception:
                    # em caso de erro, termina cutscene
                    self.finish()
        else:
            # slides fallback
            if self.t >= self.slide_time:
                self.t = 0.0
                if self.current < len(self.slides) - 1:
                    self.current += 1
                else:
                    self.finish()

    def draw(self, screen):
        # desenha vídeo frame armazenado ou slides
        if self._has_video and self._last_surface:
            try:
                surf = pygame.transform.smoothscale(self._last_surface, (S.WIDTH, S.HEIGHT))
            except Exception:
                surf = pygame.transform.scale(self._last_surface, (S.WIDTH, S.HEIGHT))
            screen.blit(surf, (0, 0))
            # dica para pular
            f = pygame.font.Font(None, int(20 * getattr(S, 'SCALE', 1.0)))
            t = f.render("Pressione Enter ou Espaço para pular", True, (200, 200, 200))
            r = t.get_rect(bottomright=(S.WIDTH - 10, S.HEIGHT - 10))
            screen.blit(t, r)
        else:
            screen.fill((5, 10, 25))
            if not self.slides:
                return
            slide = self.slides[self.current]
            if isinstance(slide, pygame.Surface):
                try:
                    img = pygame.transform.smoothscale(slide, (S.WIDTH, S.HEIGHT))
                except Exception:
                    img = pygame.transform.scale(slide, (S.WIDTH, S.HEIGHT))
                screen.blit(img, (0, 0))
            else:
                f = pygame.font.Font(None, int(36 * getattr(S, 'SCALE', 1.0)))
                lines = str(slide).split('\n')
                for i, line in enumerate(lines):
                    t = f.render(line, True, getattr(S, 'COLOR_TEXT', (220,220,220)))
                    r = t.get_rect(center=(S.WIDTH//2, S.HEIGHT//2 - 20 + i * int(40 * getattr(S, 'SCALE', 1.0))))
                    screen.blit(t, r)
                fi = pygame.font.Font(None, int(20 * getattr(S, 'SCALE', 1.0)))
                ti = fi.render("Pressione Enter ou Espaço para pular", True, (150, 150, 150))
                ri = ti.get_rect(center=(S.WIDTH//2, S.HEIGHT - int(40 * getattr(S, 'SCALE', 1.0))))
                screen.blit(ti, ri)