"""Carregamento e validação da lista de contatos a partir de um CSV."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

# Colunas obrigatórias no CSV. `anexo` é caminho relativo à raiz do projeto.
COLUNAS_OBRIGATORIAS = ("nome", "email", "anexo")


class CSVInvalidoError(Exception):
    """Lançado quando o CSV não tem as colunas esperadas ou não é legível."""


def carregar_contatos(caminho_csv: Path) -> pd.DataFrame:
    """Lê o CSV de contatos com encoding `utf-8-sig` (tolera BOM do Excel).

    Args:
        caminho_csv: caminho para o arquivo CSV.

    Returns:
        DataFrame com as colunas `nome`, `email` e `anexo`.

    Raises:
        CSVInvalidoError: se o arquivo não existir ou faltar coluna obrigatória.
    """
    if not caminho_csv.exists():
        raise CSVInvalidoError(f"Arquivo CSV não encontrado: {caminho_csv}")

    try:
        df = pd.read_csv(caminho_csv, encoding="utf-8-sig")
    except Exception as exc:  # pandas levanta exceções muito variadas
        raise CSVInvalidoError(f"Falha ao ler CSV {caminho_csv}: {exc}") from exc

    faltantes = [c for c in COLUNAS_OBRIGATORIAS if c not in df.columns]
    if faltantes:
        raise CSVInvalidoError(
            f"CSV sem coluna(s) obrigatória(s): {faltantes}. "
            f"Esperado: {list(COLUNAS_OBRIGATORIAS)}"
        )

    return df
