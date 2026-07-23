# -*- coding: utf-8 -*-
"""Diagnóstico do Renato Starter — roda checagens e imprime um relatório.

Deu qualquer problema? Rode o DIAGNOSTICO.bat e mande um print desta tela
para quem te indicou o projeto. Cada linha diz o que está OK e o que não está.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
resultados = []


def check(nome, ok, detalhe):
    resultados.append((ok, nome, detalhe))
    print(f"  [{'OK' if ok else 'X '}] {nome}: {detalhe}")


print("=" * 52)
print(" DIAGNOSTICO DO RENATO STARTER")
print("=" * 52)
print()

# 1. Python
v = sys.version.split()[0]
check("Python", sys.version_info >= (3, 10), f"{v}" + ("" if sys.version_info >= (3, 10) else " — precisa ser 3.10+"))
check("Executável", True, sys.executable)

# 2. Caminho da pasta (acento/espaço quebram alguns editores)
caminho = str(AQUI)
so_ascii = all(ord(c) < 128 for c in caminho)
check("Caminho da pasta", so_ascii, caminho + ("" if so_ascii else "  <- TEM ACENTO/CARACTERE ESPECIAL: mova para C:\\renato-main"))

# 3. Arquivos essenciais
for f in ("servidor_mcp.py", "roteador.py", "memoria.py", "gates.py", "requirements.txt"):
    check(f"Arquivo {f}", (AQUI / f).exists(), "presente" if (AQUI / f).exists() else "FALTANDO — reextraia o ZIP")

# 4. Pacote mcp
tem_mcp = importlib.util.find_spec("mcp") is not None
check("Pacote mcp", tem_mcp, "instalado" if tem_mcp else "NÃO instalado — rode o INSTALAR.bat")

# 5. O núcleo funciona? (não depende do mcp)
try:
    sys.path.insert(0, str(AQUI))
    import gates
    import memoria
    import roteador

    dom, pts = roteador.classificar("fazer o deploy do container em producao")
    check("Roteador", dom == "deploy", f"classificou deploy com {pts} pts" if dom == "deploy" else f"classificou errado: {dom}")
    check("Gate de evidência", gates.validar_evidencia("  ") is not None, "recusando recibo em branco")
    total = memoria.contar()
    check("Memória local", True, f"acessível ({total} memória(s))")
except Exception as exc:
    check("Núcleo", False, f"erro: {exc}")

# 6. Testes
r = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q", "--no-header"],
                   cwd=AQUI, capture_output=True, text=True)
linha = next((l for l in (r.stdout or "").splitlines() if "passed" in l or "failed" in l or "error" in l), "sem saída")
check("Suíte de testes", r.returncode == 0, linha.strip())

# 7. Config gerada
cfg = AQUI / "config_antigravity.json"
check("Config do Antigravity", cfg.exists(), "gerada" if cfg.exists() else "ainda não gerada — rode o INSTALAR.bat")

print()
falhas = [r for r in resultados if not r[0]]
if not falhas:
    print("  RESULTADO: TUDO VERDE — a instalação está saudável.")
    print("  Se o problema é no Antigravity, confira o Passo 4 do README")
    print("  (colar a config, salvar e clicar em Refresh).")
else:
    print(f"  RESULTADO: {len(falhas)} problema(s) — mande um print DESTA TELA para o suporte.")
