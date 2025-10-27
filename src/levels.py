# -*- coding: utf-8 -*-
from dataclasses import dataclass

@dataclass
class LevelConfig:
    name: str
    ods: str
    description: str
    words: list[str]
    spawn_factor: float
    speed_factor: float
    target_score: int
    bg_color: tuple
    grid_color: tuple
    has_boss: bool = False
    boss_words: list[str] | None = None
    boss_health: int = 0

    # novos campos para música e wallpaper
    music: str | None = None
    music_volume: float = 0.6
    wallpaper: str | None = None


LEVELS: list[LevelConfig] = [
    LevelConfig(
        name="Servidor Academico",
        ods="ODS 4 - Educacao de Qualidade",
        description="Depure dados corrompidos do SIGA e biblioteca digital.",
        words=["SPAM","FAKE","ERRO404","QUEBRADO","LINK","ENSINAR","LER","CIENCIA","VERDADE","AULA","FATEC"],
        spawn_factor=1.0,
        speed_factor=0.5,
        target_score=50,
        bg_color=(16,18,28),
        grid_color=(28,34,48),
        music='assets/musics/back_music1.mp3',
        music_volume=0.5,
        wallpaper='assets/images/wallpaper4.png',
    ),
    LevelConfig(
        name="Servidor de Infraestrutura",
        ods="ODS 9 - Industria, Inovacao e Infraestrutura",
        description="Conserte circuitos, patches e codigo limpo.",
        words=["BUG","GLITCH","ATRASO","OBSOLETO","INOVAR","CRIAR","FIX","DEPLOY","LOGICA","CLEAN"],
        spawn_factor=1.15,
        speed_factor=0.5,
        target_score=120,
        bg_color=(18,16,24),
        grid_color=(32,28,44),
        music='assets/musics/back_music1.mp3',
        music_volume=0.5,
        wallpaper='assets/images/wallpaper9.png',
    ),
    LevelConfig(
        name="Servidor de Acesso",
        ods="ODS 10 - Reducao das Desigualdades",
        description="Remova muros digitais e garanta acesso a todos.",
        words=["PAYWALL","BLOQUEIO","MURO","NEGADO","INCLUIR","ABRIR","ACESSO","TODOS","UNIR","IGUALDADE"],
        spawn_factor=1.25,
        speed_factor=0.2,
        target_score=200,
        bg_color=(14,20,20),
        grid_color=(24,36,36),
        music='assets/musics/back_music1.mp3',
        music_volume=0.5,
        wallpaper='assets/images/wallpaper10.png',
    ),
    LevelConfig(
        name="Core CPS (Boss)",
        ods="ODS 11 - Cidades e Comunidades Sustentaveis",
        description="Conter a Anomalia e restaurar a rede do CPS.",
        words=["SHUTDOWN","DELETE","FUTURO","ENERGIA","LIMPA"],
        spawn_factor=0.9,
        speed_factor=0.5,
        target_score=250,  # precisa bater 300 e derrotar o boss
        bg_color=(20,14,18),
        grid_color=(40,24,34),
        has_boss=True,
        boss_words=["RECONSTRUIR","SUSTENTABILIDADE","COLABORACAO","COMUNIDADE","GUARABYTE","ENERGIA","FATEC"],
        boss_health=7,
        music='assets/musics/back_music1.mp3',
        music_volume=0.5,
        wallpaper='assets/images/wallpaper11.png',
    ),
]
