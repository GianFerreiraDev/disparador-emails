"""Configuração central do projeto.

Carrega credenciais e parâmetros SMTP do arquivo `.env` (via `python-dotenv`).
Centralizar a configuração aqui evita que outros módulos precisem conhecer
detalhes do ambiente e facilita a troca de provedor (Gmail, Outlook, etc.).
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Carrega as variáveis definidas em .env (se existir) para o ambiente.
# Por design, .env nunca é commitado — ver .gitignore.
load_dotenv()


# ─────────────────────────── Credenciais ───────────────────────────
EMAIL_REMETENTE: str = os.getenv("EMAIL_REMETENTE", "")
EMAIL_SENHA: str = os.getenv("EMAIL_SENHA", "")

# ─────────────────────────── Servidor SMTP ─────────────────────────
SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT: int = int(os.getenv("SMTP_PORT", "465"))

# ─────────────────────────── Conteúdo ──────────────────────────────
# Assunto do e-mail — constante fixa no MVP. Evoluir para vir do template
# ou do CSV conforme o roadmap.
ASSUNTO_EMAIL: str = "Proposta personalizada — Disparador de E-mails"

# ─────────────────────────── Arquivos do projeto ───────────────────
# BASE_DIR aponta para a raiz do projeto (independente de onde o main.py
# é chamado), permitindo rodar `python main.py` de qualquer lugar.
BASE_DIR: Path = Path(__file__).resolve().parent

CSV_CONTATOS_PATH: Path = BASE_DIR / "data" / "contatos_exemplo.csv"
TEMPLATE_PATH: Path = BASE_DIR / "templates" / "email_template.html"
ANEXOS_DIR: Path = BASE_DIR / "anexos"


def credenciais_ok() -> bool:
    """Retorna True apenas se remetente e senha estão preenchidos."""
    return bool(EMAIL_REMETENTE) and bool(EMAIL_SENHA)
