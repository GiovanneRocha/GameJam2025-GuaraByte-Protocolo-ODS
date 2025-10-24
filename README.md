
# GuaraByte: Protocolo ODS (portrait, modular)

**Engine:** Pygame  \
**Layout:** Janela vertical (portrait) com **escala dinâmica**  \
**Estilo:** Digitação (inspirado em zty.pe)

## Novidades desta versão
- ✔️ **Escala adaptativa** (se ajusta à tela do usuário mantendo 9:16)  
- ✔️ **Textos e caixas se autoajustam** (sem cortes)  
- ✔️ **Inimigos ricocheteiam nas paredes laterais** (não saem da tela)  
- ✔️ **Troca de alvo no Boss** ao iniciar nova palavra  
- ✔️ **Palavras duplicadas**: concluir uma remove **todas iguais** em tela  
- ✔️ **Metas**: **300 pontos** por nível para avançar (no Boss: 300 + derrotar o Boss)

## Estrutura
```
src/
  main.py        # loop de jogo, estados, gravação de demo
  settings.py    # resolução base, escala, ajustes de gameplay
  levels.py      # definição das fases (todas com target_score = 300)
  utils.py       # helpers de UI (grid, fontes, clamp, fit-text)
  ui.py          # HUD, banner do Boss, instruções
  assets.py      # carregamento de SFX (CC0)
  entities.py    # WordEnemy (com bounce), Boss
assets/
  sfx/           # type_ok.wav, word_clean.wav, boss_hit.wav

README.md
requirements.txt
```

## Como rodar
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

## Gravar GIF demo (autoplay)
```bash
python src/main.py --record-demo 10  # salva demo/demo.gif
```

## Build do executável (Windows)
```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --name GuaraByte src/main.py --paths src --add-data "assets:assets"
```
