from __future__ import annotations

from collections import Counter

Jogo = tuple[int, ...]


def _normalizar_jogo(jogo: list[int] | tuple[int, ...]) -> Jogo:
    dezenas = tuple(sorted(jogo))
    if len(dezenas) != 6 or len(set(dezenas)) != 6:
        raise ValueError("Jogo deve conter 6 dezenas distintas")
    if not all(1 <= dezena <= 60 for dezena in dezenas):
        raise ValueError("Dezenas devem estar entre 1 e 60")
    return dezenas


def evitar_sequencias_longas(jogo: list[int] | tuple[int, ...], tamanho_maximo: int = 3) -> bool:
    dezenas = _normalizar_jogo(jogo)
    maior_sequencia = 1
    sequencia_atual = 1
    for atual, proxima in zip(dezenas, dezenas[1:]):
        if proxima == atual + 1:
            sequencia_atual += 1
            maior_sequencia = max(maior_sequencia, sequencia_atual)
        else:
            sequencia_atual = 1
    return maior_sequencia <= tamanho_maximo


def evitar_todos_pares_ou_todos_impares(jogo: list[int] | tuple[int, ...]) -> bool:
    dezenas = _normalizar_jogo(jogo)
    pares = sum(1 for dezena in dezenas if dezena % 2 == 0)
    return 0 < pares < len(dezenas)


def evitar_concentracao_faixa(jogo: list[int] | tuple[int, ...], max_por_faixa: int = 4) -> bool:
    dezenas = _normalizar_jogo(jogo)
    faixas = Counter((dezena - 1) // 10 for dezena in dezenas)
    return max(faixas.values(), default=0) <= max_por_faixa


def jogo_valido_basico(jogo: list[int] | tuple[int, ...]) -> bool:
    return (
        evitar_sequencias_longas(jogo)
        and evitar_todos_pares_ou_todos_impares(jogo)
        and evitar_concentracao_faixa(jogo)
    )
