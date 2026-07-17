@echo off
chcp 65001 >nul
title Instalador do Renato Starter
cd /d "%~dp0"

echo.
echo  ============================================
echo   RENATO STARTER - instalador automatico
echo  ============================================
echo.

rem -- localiza o Python (evitando o atalho falso da Loja do Windows)
set "PY="
python --version >nul 2>&1
if not errorlevel 1 set "PY=python"
if not defined PY (
  py -3 --version >nul 2>&1
  if not errorlevel 1 set "PY=py -3"
)
if not defined PY (
  echo  [X] Python nao encontrado neste computador.
  echo.
  echo  Como resolver ^(2 minutos^):
  echo   1. Vou abrir a pagina de download do Python agora.
  echo   2. Clique no botao amarelo "Download Python 3.x".
  echo   3. Abra o instalador e MARQUE A CAIXINHA
  echo      "Add python.exe to PATH" antes de clicar Install Now.
  echo   4. Quando terminar, rode este INSTALAR.bat de novo.
  echo.
  start https://www.python.org/downloads/
  pause
  exit /b 1
)

%PY% instalar.py
echo.
pause
