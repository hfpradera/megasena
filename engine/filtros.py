from __future__ import annotations

import itertools
import math
from collections import Counter
from typing import Dict, Iterable, List, Sequence, Tuple

PRIMOS = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59}


Jogo = Sequence[int]
Historico = Sequence[Sequence[int]]


def _media(valores: Sequence[float]) -> float:
    if not valores:
        return 0.0
    return sum(valores) / len(valores)


def filtro_distancia(jogo: Jogo) -> float:
    ordenado = sorted(jogo)
    return float(ordenado[-1] - ordenado[0])


def filtro_media_numeros(jogo: Jogo) -> float:
    return _media(jogo)


def filtro_media_unidades(jogo: Jogo) -> float:
    return _media([n % 10 for n in jogo])


def filtro_media_dezenas(jogo: Jogo) -> float:
    return _media([n // 10 for n in jogo])


def filtro_media_pares(jogo: Jogo) -> float:
    pares = [n for n in jogo if n % 2 == 0]
    return _media(pares)


def filtro_media_impares(jogo: Jogo) -> float:
    impares = [n for n in jogo if n % 2 == 1]
    return _media(impares)


def filtro_media_primos(jogo: Jogo) -> float:
    primos = [n for n in jogo if n in PRIMOS]
    return _media(primos)


def filtro_desvio_padrao(jogo: Jogo) -> float:
    m = filtro_media_numeros(jogo)
    return math.sqrt(_media([(n - m) ** 2 for n in jogo]))


FUNCOES_FILTRO = {
    "distancia": filtro_distancia,
    "media_numeros": filtro_media_numeros,
    "media_unidades": filtro_media_unidades,
    "media_dezenas": filtro_media_dezenas,
    "media_pares": filtro_media_pares,
    "media_impares": filtro_media_impares,
    "media_primos": filtro_media_primos,
    "desvio_padrao": filtro_desvio_padrao,
}


def calcular_filtros(jogo: Jogo) -> Dict[str, float]:
    return {nome: fn(jogo) for nome, fn in FUNCOES_FILTRO.items()}


def aprender_filtros(historico: Historico, percentual: float = 70) -> Dict[str, set]:
    """
    Aprende os valores aceitos por filtro usando frequência acumulada.
    Mantém os valores mais frequentes até cobrir `percentual`%% do histórico.
    """
    total = len(historico)
    if total == 0:
        return {k: set() for k in FUNCOES_FILTRO}

    dist = {k: Counter() for k in FUNCOES_FILTRO}
    for jogo in historico:
        vals = calcular_filtros(jogo)
        for nome, valor in vals.items():
            dist[nome][round(valor, 2)] += 1

    aceitos: Dict[str, set] = {}
    alvo = total * (percentual / 100.0)
    for nome, cnt in dist.items():
        cumul = 0
        ok = set()
        for valor, freq in cnt.most_common():
            ok.add(valor)
            cumul += freq
            if cumul >= alvo:
                break
        aceitos[nome] = ok
    return aceitos


def _avaliar_jogo_6(jogo6: Jogo, filtros_aceitos: Dict[str, set]) -> Tuple[bool, List[str]]:
    valores = calcular_filtros(jogo6)
    passados = [
        nome
        for nome, valor in valores.items()
        if round(valor, 2) in filtros_aceitos.get(nome, set())
    ]
    return True, passados


def jogo_valido(
    jogo: Jogo,
    historico: Historico,
    percentual: float = 70,
    perc_acerto: float = 70,
) -> Tuple[bool, List[str]]:
    """
    Valida jogo conforme lógica tipo Delphi:
    - aprende valores aceitos por filtro do histórico
    - exige passar em quantidade mínima de filtros (perc_acerto)
    - para jogos > 6 dezenas, avalia combinações internas de 6
    """
    filtros_aceitos = aprender_filtros(historico, percentual=percentual)
    minimo = math.ceil(len(FUNCOES_FILTRO) * (perc_acerto / 100.0))

    jogo_ord = sorted(set(jogo))
    if len(jogo_ord) < 6:
        return False, []

    candidatos = [jogo_ord] if len(jogo_ord) == 6 else list(itertools.combinations(jogo_ord, 6))

    melhor: List[str] = []
    for base in candidatos:
        _, passados = _avaliar_jogo_6(base, filtros_aceitos)
        if len(passados) > len(melhor):
            melhor = passados
        if len(passados) >= minimo:
            return True, passados

    return False, melhor
