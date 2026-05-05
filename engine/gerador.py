from __future__ import annotations

import random
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from .filtros import jogo_valido


def carregar_historico(caminho: str = "data/resultadosMega.txt") -> List[List[int]]:
    p = Path(caminho)
    if not p.exists():
        return []

    historico: List[List[int]] = []
    for linha in p.read_text(encoding="utf-8").splitlines():
        partes = [x for x in linha.replace(";", " ").replace(",", " ").split() if x.isdigit()]
        if len(partes) >= 6:
            jogo = sorted({int(x) for x in partes[:6]})
            if len(jogo) == 6:
                historico.append(jogo)
    return historico


def estrategia_por_orcamento(orcamento: float) -> Dict[str, float | int | str]:
    if orcamento < 50:
        return {"dezenas": 6, "qtd": 5, "percentual": 68, "perc_acerto": 68, "nome": "Conservadora"}
    if orcamento < 150:
        return {"dezenas": 7, "qtd": 8, "percentual": 70, "perc_acerto": 70, "nome": "Balanceada"}
    return {"dezenas": 8, "qtd": 12, "percentual": 72, "perc_acerto": 72, "nome": "Agressiva"}


def gerar_jogos(
    historico: Sequence[Sequence[int]],
    qtd: int,
    dezenas: int = 6,
    percentual: float = 70,
    perc_acerto: float = 70,
    tentativas_max: int = 25000,
) -> List[Dict]:
    universo = list(range(1, 61))
    sorteados = {tuple(sorted(j)) for j in historico}
    gerados = set()
    saida: List[Dict] = []

    tentativas = 0
    while len(saida) < qtd and tentativas < tentativas_max:
        tentativas += 1
        jogo = tuple(sorted(random.sample(universo, dezenas)))

        if jogo in gerados or jogo in sorteados:
            continue

        valido, filtros = jogo_valido(jogo, historico, percentual=percentual, perc_acerto=perc_acerto)
        if not valido:
            continue

        gerados.add(jogo)
        saida.append({"jogo": jogo, "filtros_ok": filtros})

    return saida
