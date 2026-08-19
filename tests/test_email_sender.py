"""Testes do EmailSender com SMTP mockado.

Verificamos que a montagem do MIME e o ciclo de login/send_message/quit
ocorrem na ordem e com os argumentos esperados, sem tocar em rede.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.email_sender import EmailSender


class FakeSMTP:
    """Stub mínimo de SMTP_SSL para uso em testes."""

    def __init__(self, server: str, port: int) -> None:
        self.server = server
        self.port = port
        self.logged_in_as: tuple[str, str] | None = None
        self.sent_messages = []
        self.quit_called = False

    def login(self, user: str, password: str) -> None:
        self.logged_in_as = (user, password)

    def send_message(self, msg) -> None:
        self.sent_messages.append(msg)

    def quit(self) -> None:
        self.quit_called = True

    # Protocolo de context manager — EmailSender usa `with smtp_factory(...) as smtp`.
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.quit()


@pytest.fixture
def fake_smtp() -> FakeSMTP:
    return FakeSMTP("smtp.test", 465)


def test_envio_sem_anexo_chama_login_send_e_quit(fake_smtp):
    sender = EmailSender(
        remetente="remetente@test.com",
        senha="segredo",
        servidor="smtp.test",
        porta=465,
        smtp_factory=lambda s, p: fake_smtp,
    )

    sender.enviar(
        destinatario="dest@test.com",
        assunto="Olá",
        corpo_html="<p>Oi {nome}</p>",
        caminho_anexo=None,
    )

    assert fake_smtp.logged_in_as == ("remetente@test.com", "segredo")
    assert len(fake_smtp.sent_messages) == 1
    assert fake_smtp.quit_called is True

    msg = fake_smtp.sent_messages[0]
    assert msg["To"] == "dest@test.com"
    assert msg["Subject"] == "Olá"


def test_envio_com_anexo_anexa_arquivo(tmp_path: Path, fake_smtp):
    anexo = tmp_path / "doc.pdf"
    anexo.write_bytes(b"%PDF-1.4 fake content")

    sender = EmailSender(
        remetente="r@t.com",
        senha="x",
        servidor="smtp.test",
        porta=465,
        smtp_factory=lambda s, p: fake_smtp,
    )

    sender.enviar(
        destinatario="d@t.com",
        assunto="Anexo",
        corpo_html="<p>x</p>",
        caminho_anexo=anexo,
    )

    msg = fake_smtp.sent_messages[0]
    # EmailMessage adiciona o anexo como um novo payload — checamos que
    # o nome do arquivo aparece em alguma parte da mensagem serializada.
    assert "doc.pdf" in msg.as_string()


def test_anexo_inexistente_levanta_filenotfound():
    sender = EmailSender("r@t.com", "x", "smtp.test", 465)
    with pytest.raises(FileNotFoundError):
        sender.enviar(
            destinatario="d@t.com",
            assunto="x",
            corpo_html="<p>x</p>",
            caminho_anexo=Path("/nao/existe.pdf"),
        )


def test_smtp_factory_recebe_servidor_e_porta():
    recebido = {}

    def factory(server: str, port: int):
        recebido["server"] = server
        recebido["port"] = port
        return MagicMock()

    sender = EmailSender(
        remetente="r@t.com",
        senha="x",
        servidor="smtp.exemplo.com",
        porta=587,
        smtp_factory=factory,
    )
    sender.enviar("d@t.com", "s", "<p>x</p>", None)

    assert recebido == {"server": "smtp.exemplo.com", "port": 587}
