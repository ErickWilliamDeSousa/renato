# -*- coding: utf-8 -*-
"""Instalador do Renato Starter — pensado para quem nunca programou.

Faz, nesta ordem, avisando cada passo:
  1. instala as bibliotecas necessárias
  2. roda os 10 testes (prova de que está saudável)
  3. gera a configuração do Antigravity/IDE com os caminhos CERTOS
     deste computador (config_antigravity.json) e copia para o Ctrl+V

Uso normal:  duplo clique em INSTALAR.bat (que chama este arquivo).
Uso técnico: python instalar.py [--silencioso]
"""
import json
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SILENCIOSO = "--silencioso" in sys.argv


def passo(n, msg):
    print(f"\n[{n}/3] {msg}")


def falha(msg, dica):
    print(f"\n  [X] {msg}")
    print(f"  Como resolver: {dica}")
    sys.exit(1)


def main():
    if sys.version_info < (3, 10):
        falha(f"Seu Python é {sys.version.split()[0]}, mas o Renato precisa do 3.10 ou mais novo.",
              "instale o Python atual em python.org/downloads (marcando 'Add python.exe to PATH') "
              "e rode o INSTALAR.bat de novo.")
    print(f"  Python encontrado: {sys.version.split()[0]}  OK")

    # 1 — dependências -----------------------------------------------------
    passo(1, "Instalando as bibliotecas (pode levar 1-2 minutos)...")
    r = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(AQUI / "requirements.txt"), "-q"],
        cwd=AQUI,
    )
    if r.returncode != 0:
        falha("A instalação das bibliotecas falhou.",
              "confira sua internet e rode o INSTALAR.bat de novo. "
              "Se persistir, mande uma foto desta janela para quem te indicou o projeto.")
    r = subprocess.run([sys.executable, "-c", "import mcp"], capture_output=True)
    if r.returncode != 0:
        falha("As bibliotecas instalaram, mas o pacote 'mcp' não importa neste Python.",
              "você provavelmente tem mais de um Python na máquina. Feche tudo, rode o "
              "INSTALAR.bat de novo e, se repetir, rode o DIAGNOSTICO.bat e mande o print.")
    print("  Bibliotecas instaladas.  OK")

    # 2 — testes -----------------------------------------------------------
    passo(2, "Rodando os testes de saúde da semente...")
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q"],
        cwd=AQUI, capture_output=True, text=True,
    )
    saida = (r.stdout or "") + (r.stderr or "")
    if r.returncode != 0 or "passed" not in saida:
        print(saida[-800:])
        falha("Algum teste falhou.",
              "rode o INSTALAR.bat de novo; se persistir, mande uma foto desta janela.")
    resumo = [l for l in saida.splitlines() if "passed" in l]
    print(f"  Testes: {resumo[-1].strip() if resumo else 'verdes'}  OK")

    # 3 — configuração do IDE ---------------------------------------------
    passo(3, "Gerando a configuração do Antigravity com os caminhos deste computador...")
    python_exe = Path(sys.executable).as_posix()
    servidor = (AQUI / "servidor_mcp.py").as_posix()
    config = {
        "mcpServers": {
            "renato-starter": {
                "command": python_exe,
                "args": [servidor],
            }
        }
    }
    destino = AQUI / "config_antigravity.json"
    destino.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Arquivo criado: {destino.name}  OK")

    copiado = False
    if not SILENCIOSO:
        try:
            subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 f"Get-Content -Raw '{destino}' | Set-Clipboard"],
                check=True, capture_output=True, timeout=20,
            )
            copiado = True
        except Exception:
            pass
        try:
            subprocess.Popen(["notepad", str(destino)])
        except Exception:
            pass

    # aviso honesto sobre acentos no caminho (fonte comum de erro no MCP)
    caminho_ascii = all(ord(c) < 128 for c in str(AQUI))

    print("""
  ==========================================
   TUDO PRONTO!
  ==========================================
""")
    if copiado:
        print("  A configuração JÁ ESTÁ COPIADA (é só dar Ctrl+V no Antigravity).")
    print("  Ela também abriu no Bloco de Notas e está salva em config_antigravity.json.")
    if not caminho_ascii:
        print("""
  [!] ATENÇÃO: o caminho desta pasta tem acento ou caractere especial.
      Alguns editores falham com isso. Se o Antigravity não conectar,
      mova a pasta para C:\\renato e rode o INSTALAR.bat de novo.""")
    print("""
  PRÓXIMO PASSO — no Antigravity:
   1. Painel do Agente  >  ícone de MCP / plug  >  Manage MCP Servers
   2. Abra o arquivo de configuração (View raw config)
   3. Cole (Ctrl+V), salve e clique em Refresh
   4. No chat, digite:
      Chame a ferramenta verificar do renato-starter
      (a resposta certa é "TUDO VERDE")

  O passo a passo com detalhes está no README.md desta pasta.
""")


if __name__ == "__main__":
    main()
