@echo off
chcp 65001 >nul
title Diagnostico do Renato Starter
cd /d "%~dp0"

set "PY="
python --version >nul 2>&1
if not errorlevel 1 set "PY=python"
if not defined PY (
  py -3 --version >nul 2>&1
  if not errorlevel 1 set "PY=py -3"
)
if not defined PY (
  echo  [X] Python nao encontrado neste computador.
  echo      Siga o Passo 2 do README ^(instalar o Python marcando "Add to PATH"^)
  echo      e rode este DIAGNOSTICO.bat de novo.
  pause
  exit /b 1
)

%PY% diagnostico.py
echo.
echo  Tire um print desta janela se precisar de ajuda.
pause
