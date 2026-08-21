"""Ponto de entrada do Disparador de E-mails.

Fluxo:
    1. Carrega contatos do CSV.
    2. Para cada contato: renderiza template, monta e-mail e envia.
    3. Falha em um contato não interrompe os demais (princípio do MVP).
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import config
from src.contact_loader import carregar_contatos, CSVInvalidoError
from src.email_sender import EmailSender
from src.template_engine import carregar_template, renderizar

logger = logging.getLogger("disparador")


def _configurar_logging() -> None:
    """Logging no console com timestamp, nível e mensagem."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
    )
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)


def _processar_contato(linha, sender: EmailSender, template: str, base_dir: Path) -> str:
    """Tenta enviar um e-mail. Retorna 'ok' ou 'falha' para o relatório."""
    nome = str(linha["nome"]).strip()
    email = str(linha["email"]).strip()
    anexo_relativo = str(linha["anexo"]).strip()

    corpo = renderizar(template, {"nome": nome})
    anexo_path: Path | None = None
    if anexo_relativo:
        candidato = (base_dir / anexo_relativo).resolve()
        if not candidato.exists():
            logger.warning(
                "Anexo '%s' ausente para %s — enviando sem anexo.",
                anexo_relativo,
                email,
            )
        else:
            anexo_path = candidato

    sender.enviar(email, config.ASSUNTO_EMAIL, corpo, anexo_path)
    return "ok"


def main() -> int:
    _configurar_logging()

    if not config.credenciais_ok():
        logger.error(
            "Credenciais ausentes no .env (EMAIL_REMETENTE / EMAIL_SENHA). Abortando."
        )
        return 1

    sender = EmailSender(
        remetente=config.EMAIL_REMETENTE,
        senha=config.EMAIL_SENHA,
        servidor=config.SMTP_SERVER,
        porta=config.SMTP_PORT,
    )

    try:
        contatos = carregar_contatos(config.CSV_CONTATOS_PATH)
        template = carregar_template(config.TEMPLATE_PATH)
    except (CSVInvalidoError, FileNotFoundError) as exc:
        logger.error("Erro de configuração: %s", exc)
        return 1

    logger.info("Iniciando envio para %d contato(s).", len(contatos))

    sucessos = 0
    falhas = 0
    for _, linha in contatos.iterrows():
        email_dest = str(linha["email"]).strip()
        try:
            _processar_contato(linha, sender, template, config.BASE_DIR)
        except Exception as exc:  # falha isolada por contato
            falhas += 1
            logger.error("Falha ao enviar para %s: %s", email_dest, exc)
            continue

        sucessos += 1
        logger.info("Enviado para %s.", email_dest)

    logger.info("Resumo: %d enviado(s), %d falha(s).", sucessos, falhas)
    return 0 if falhas == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
