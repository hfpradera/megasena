from __future__ import annotations

import random

from engine.filtros import jogo_valido_basico


class LimiteTentativasError(RuntimeError):
    pass


def gerar_jogo_valido(max_tentativas: int = 5000) -> tuple[int, ...]:
    for _ in range(max_tentativas):
        jogo = tuple(sorted(random.sample(range(1, 61), 6)))
        if jogo_valido_basico(jogo):
            return jogo
    raise LimiteTentativasError("Não foi possível gerar jogo válido no limite de tentativas")


def gerar_varios_jogos(quantidade: int = 5, max_tentativas: int = 5000) -> list[tuple[int, ...]]:
    if quantidade < 1:
        return []

    jogos: set[tuple[int, ...]] = set()
    tentativas = 0
    limite_global = max_tentativas * max(quantidade, 1)

    while len(jogos) < quantidade and tentativas < limite_global:
        jogos.add(gerar_jogo_valido(max_tentativas=max_tentativas))
        tentativas += 1

    return sorted(jogos)
