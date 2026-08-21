"""Renderização do corpo do e-mail a partir de um template HTML.

No MVP usa `str.format()` com placeholders simples (`{nome}`). O roadmap
prevê migração para Jinja2 (Fase 2) para suportar lógica condicional e
loops nos templates.
"""

from __future__ import annotations

from pathlib import Path
from typing import Mapping


def carregar_template(caminho: Path) -> str:
    """Lê o template do disco usando UTF-8 (acentos preservados)."""
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()


def renderizar(template: str, contexto: Mapping[str, object]) -> str:
    """Substitui placeholders `{chave}` pelos valores do contexto.

    Levanta `KeyError` se o template referenciar uma chave ausente no
    contexto — preferível a enviar e-mail com `{nome}` literal visível
    ao destinatário.
    """
    return template.format(**contexto)
