@echo off
REM ==============================================
REM  Rodar Jogo (Python/Pygame) sem console visível via VBS
REM  Este .bat é chamado pelo VBS. Pode ser executado sozinho também.
REM  Coloque este arquivo NA MESMA PASTA do seu main.py
REM ==============================================

REM Define a pasta do script
set SCRIPT_DIR=%~dp0
pushd "%SCRIPT_DIR%"

REM (Opcional) Ative o ambiente virtual se existir .venv
if exist .venv\Scripts\activate.bat (
  call .venv\Scripts\activate.bat
)

REM Executa o jogo
python "%SCRIPT_DIR%main.py"

popd
