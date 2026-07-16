# Push com token lido do .env — o valor nunca é impresso nem persistido.
# O token vai como credencial embutida numa URL usada SÓ neste comando
# (o remote 'origin' configurado no repo continua limpo, sem token).
import subprocess
import sys
from pathlib import Path

REPO = Path(r"C:\Users\erick\Desktop\renato-publico")
ENV = REPO / ".env"

token = ""
for linha in ENV.read_text(encoding="utf-8", errors="ignore").splitlines():
    if linha.strip().startswith("GITHUB_TOKEN="):
        token = linha.split("=", 1)[1].strip().strip('"').strip("'")
        break

if not token:
    print("ERRO: GITHUB_TOKEN vazio no .env — cole a chave e salve o arquivo.")
    sys.exit(1)

url = f"https://{token}@github.com/ErickWilliamDeSousa/renato.git"
r = subprocess.run(
    ["git", "-C", str(REPO), "push", url, "main:main"],
    capture_output=True, text=True,
)
saida = (r.stdout + r.stderr).replace(token, "[TOKEN]")
print(saida)
print("push:", "OK" if r.returncode == 0 else f"FALHOU (rc={r.returncode})")
sys.exit(r.returncode)
