"""Envio de e-mails via SMTP_SSL.

Encapsula a montagem do MIME (HTML + anexo), conexão segura e o envio.
A classe `EmailSender` aceita um servidor SMTP injetado (default:
`smtplib.SMTP_SSL`), o que facilita mockar nos testes unitários.
"""

from __future__ import annotations

import mimetypes
import smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import Protocol


class SMTPClient(Protocol):
    """Subconjunto de `smtplib.SMTP_SSL` que usamos — facilita mock nos testes."""

    def login(self, user: str, password: str) -> object: ...
    def send_message(self, msg: EmailMessage) -> object: ...
    def quit(self) -> object: ...


class EmailSender:
    """Envia e-mails HTML com anexo opcional via SMTP_SSL."""

    def __init__(
        self,
        remetente: str,
        senha: str,
        servidor: str,
        porta: int,
        smtp_factory=smtplib.SMTP_SSL,
    ) -> None:
        self.remetente = remetente
        self.senha = senha
        self.servidor = servidor
        self.porta = porta
        self._smtp_factory = smtp_factory

    # ─────────────── API pública ───────────────
    def enviar(
        self,
        destinatario: str,
        assunto: str,
        corpo_html: str,
        caminho_anexo: Path | None,
    ) -> None:
        """Monta o e-mail e envia. Levanta exceção em caso de falha de SMTP."""
        mensagem = self._montar_mensagem(destinatario, assunto, corpo_html, caminho_anexo)

        with self._smtp_factory(self.servidor, self.porta) as smtp:
            smtp.login(self.remetente, self.senha)
            smtp.send_message(mensagem)

    # ─────────────── Internos ───────────────
    @staticmethod
    def _montar_mensagem(
        destinatario: str,
        assunto: str,
        corpo_html: str,
        caminho_anexo: Path | None,
    ) -> EmailMessage:
        msg = EmailMessage()
        msg["From"] = ""  # preenchido pelo caller via remetente no login
        msg["To"] = destinatario
        msg["Subject"] = assunto
        msg.set_content("Este e-mail requer um cliente com suporte a HTML.")
        msg.add_alternative(corpo_html, subtype="html")

        if caminho_anexo is not None:
            EmailSender._anexar_arquivo(msg, caminho_anexo)

        return msg

    @staticmethod
    def _anexar_arquivo(msg: EmailMessage, caminho: Path) -> None:
        if not caminho.exists():
            raise FileNotFoundError(f"Anexo não encontrado: {caminho}")

        tipo_mime, _ = mimetypes.guess_type(caminho.name)
        if tipo_mime is None:
            tipo_mime = "application/octet-stream"
        tipo_principal, sub_tipo = tipo_mime.split("/", 1)

        with open(caminho, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype=tipo_principal,
                subtype=sub_tipo,
                filename=caminho.name,
            )
