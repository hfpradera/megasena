from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Concurso:
    numero: int
    dezenas: tuple[int, ...]


class HistoricoInvalidoError(ValueError):
    """Erro para linhas de histórico mal formatadas."""


def _normalizar_tokens(linha: str) -> list[str]:
    return [token for token in linha.replace(";", " ").replace(",", " ").split() if token]


def _parse_linha(linha: str, numero_linha: int) -> Concurso:
    tokens = _normalizar_tokens(linha)
    if len(tokens) < 7:
        raise HistoricoInvalidoError(
            f"Linha {numero_linha}: esperado concurso + 6 dezenas, recebido {tokens!r}"
        )

    try:
        numero = int(tokens[0])
        dezenas = tuple(sorted(int(token) for token in tokens[1:7]))
    except ValueError as exc:
        raise HistoricoInvalidoError(
            f"Linha {numero_linha}: valores não numéricos em {tokens!r}"
        ) from exc

    if len(set(dezenas)) != 6 or not all(1 <= dezena <= 60 for dezena in dezenas):
        raise HistoricoInvalidoError(
            f"Linha {numero_linha}: dezenas inválidas {dezenas!r}"
        )

    return Concurso(numero=numero, dezenas=dezenas)


def ler_historico(caminho: str | Path = "data/resultadosMega.txt") -> list[Concurso]:
    arquivo = Path(caminho)
    if not arquivo.exists():
        return []

    concursos: list[Concurso] = []
    for idx, linha in enumerate(arquivo.read_text(encoding="utf-8").splitlines(), start=1):
        conteudo = linha.strip()
        if not conteudo or conteudo.startswith("#"):
            continue
        concursos.append(_parse_linha(conteudo, idx))
    return concursos


def ultimos_concursos(historico: Iterable[Concurso], limite: int = 10) -> list[Concurso]:
    return sorted(historico, key=lambda item: item.numero, reverse=True)[:limite]
