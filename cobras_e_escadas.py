import random

CASA_INICIAL, CASA_FINAL = 1, 36
QUANTIDADE_PARTIDAS = 10_000
SEMENTE_ALEATORIA = 67

TABULEIRO = [
    [36, 35, 34, 33, 32, 31],
    [25, 26, 27, 28, 29, 30],
    [24, 23, 22, 21, 20, 19],
    [13, 14, 15, 16, 17, 18],
    [12, 11, 10, 9, 8, 7],
    [1, 2, 3, 4, 5, 6],
]

ESCADAS = {3: 16, 5: 7, 15: 25, 18: 20, 21: 32}
COBRAS = {12: 2, 14: 11, 17: 4, 31: 19, 35: 22}


def lancar_dado() -> int:
    return random.randint(1, 6)


def mover(posicao: int, dado: int, chance_escada: float = 1.0) -> int:
    posicao += dado

    if posicao >= CASA_FINAL:
        return CASA_FINAL

    if posicao in ESCADAS and (chance_escada == 1 or random.random() < chance_escada):
        return ESCADAS[posicao]

    if posicao in COBRAS:
        return COBRAS[posicao]

    return posicao


def venceu(posicao: int) -> bool:
    return posicao >= CASA_FINAL


def jogar_partida(
    mostrar: bool = True,
    chance_escada: float = 1.0,
    inicio_jogador2: int = CASA_INICIAL,
    imunidade_jogador2: bool = False,
) -> tuple[int, int, int]:
    posicoes = [CASA_INICIAL, inicio_jogador2]
    total_cobras = 0
    total_lancamentos = 0
    imunidade_usada = False

    while True:
        for jogador in range(2):
            dado = lancar_dado()
            total_lancamentos += 1
            posicao_anterior = posicoes[jogador]

            caiu_cobra = posicao_anterior + dado in COBRAS

            if caiu_cobra:
                total_cobras += 1

            if (
                jogador == 1
                and imunidade_jogador2
                and caiu_cobra
                and not imunidade_usada
            ):
                posicoes[jogador] = posicao_anterior + dado
                imunidade_usada = True
            else:
                posicoes[jogador] = mover(posicao_anterior, dado, chance_escada)

            if mostrar:
                print(
                    f"Jogador {jogador + 1}: "
                    f"casa {posicao_anterior:2} + dado {dado} "
                    f"-> casa {posicoes[jogador]:2}"
                )

            if venceu(posicoes[jogador]):
                if mostrar:
                    print(f"\nJogador {jogador + 1} venceu!")
                    print(f"Encontros com cobras: {total_cobras}")
                    print(f"Total de lançamentos: {total_lancamentos}")

                return jogador + 1, total_cobras, total_lancamentos


def simular_partidas(quantidade: int = QUANTIDADE_PARTIDAS) -> None:
    vitorias = [0, 0]
    total_cobras = 0

    for _ in range(quantidade):
        vencedor, cobras, _ = jogar_partida(mostrar=False)

        vitorias[vencedor - 1] += 1
        total_cobras += cobras

    print(f"Partidas simuladas: {quantidade}\n")

    for jogador, total in enumerate(vitorias, start=1):
        probabilidade = total / quantidade * 100

        print(f"Jogador {jogador}: {total} vitórias ({probabilidade:.2f}%)")

    media_cobras = total_cobras / quantidade

    print(f"\nEncontros com cobras: {total_cobras}")
    print(f"Média de cobras por partida: {media_cobras:.2f}")


def simular_escadas_50(quantidade: int = QUANTIDADE_PARTIDAS) -> None:
    total_lancamentos = 0

    for _ in range(quantidade):
        _, _, lancamentos = jogar_partida(mostrar=False, chance_escada=0.5)

        total_lancamentos += lancamentos

    media = total_lancamentos / quantidade

    print(f"Partidas simuladas: {quantidade}")
    print(f"Total de lançamentos: {total_lancamentos}")
    print(f"Média de lançamentos por partida: {media:.2f}")


def simular_posicao_inicial(quantidade: int = QUANTIDADE_PARTIDAS) -> None:
    melhor_casa = None
    menor_diferenca = float("inf")
    melhor_probabilidade = 0

    for casa in range(CASA_INICIAL, CASA_FINAL):
        vitorias = 0

        for _ in range(quantidade):
            vencedor, _, _ = jogar_partida(mostrar=False, inicio_jogador2=casa)

            if vencedor == 1:
                vitorias += 1

        probabilidade = vitorias / quantidade * 100
        diferenca = abs(probabilidade - 50)

        if diferenca < menor_diferenca:
            melhor_casa = casa
            menor_diferenca = diferenca
            melhor_probabilidade = probabilidade

    print(f"Melhor casa inicial para o jogador 2: {melhor_casa}")
    print(f"Chance estimada do jogador 1: {melhor_probabilidade:.2f}%")
    print(f"Chance estimada do jogador 2: {100 - melhor_probabilidade:.2f}%")


def simular_imunidade(quantidade: int = QUANTIDADE_PARTIDAS) -> None:
    vitorias = 0

    for _ in range(quantidade):
        vencedor, _, _ = jogar_partida(mostrar=False, imunidade_jogador2=True)

        if vencedor == 1:
            vitorias += 1

    probabilidade = vitorias / quantidade * 100

    print(f"Partidas simuladas: {quantidade}")
    print(f"Vitórias do jogador 1: {vitorias}")
    print(f"Chance estimada do jogador 1: {probabilidade:.2f}%")


def exibir_secao(titulo: str) -> None:
    print(f"\n{titulo}\n{'-' * len(titulo)}")


def main() -> None:
    random.seed(SEMENTE_ALEATORIA)

    print("COBRAS E ESCADAS")
    print(f"Tabuleiro: 6 x 6 | Semente aleatória: {SEMENTE_ALEATORIA}")

    exibir_secao("Perguntas 1 e 2 | Vitórias e encontros com cobras")
    simular_partidas()

    exibir_secao("Pergunta 3 | Escadas com 50% de chance de uso")
    simular_escadas_50()

    exibir_secao("Pergunta 4 | Posição inicial para equilibrar o jogo")
    simular_posicao_inicial()

    exibir_secao("Pergunta 5 | Imunidade à primeira cobra do jogador 2")
    simular_imunidade()


if __name__ == "__main__":
    main()
