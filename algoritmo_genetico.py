import math
import random


# =========================================================
# HIPERPARÂMETROS - CONFIGURAÇÃO FORTE
# =========================================================
TAM_POPULACAO = 80
MAX_GERACOES = 600
TAXA_MUTACAO = 0.08
TAXA_CROSSOVER = 0.85
TAM_TORNEIO = 4

# =========================================================
# HIPERPARÂMETROS - CONFIGURAÇÃO FRACA
# =========================================================
# TAM_POPULACAO = 40
# MAX_GERACOES = 200
# TAXA_MUTACAO = 0.02
# TAXA_CROSSOVER = 0.75
# TAM_TORNEIO = 2


# =========================================================
# CLASSE
# =========================================================

class AlgoritmoGenetico:

    def __init__(self, coordenadas):

        self.coordenadas = coordenadas
        self.numcidades = len(coordenadas)

        self.historico_melhor = []
        self.historico_medio = []

        self.melhor_distancia_global = float("inf")
        self.melhor_rota_global = None

    # =====================================================
    # DISTÂNCIA EUCLIDIANA
    # =====================================================

    def calcular_distancia(self, a, b):

        return math.sqrt(
            (a[0] - b[0])**2 +
            (a[1] - b[1])**2
        )

    # =====================================================
    # DISTÂNCIA TOTAL
    # =====================================================

    def calcular_distancia_total(self, rota):

        total = 0.0

        for i in range(len(rota) - 1):

            cidade_a = self.coordenadas[rota[i]]
            cidade_b = self.coordenadas[rota[i + 1]]

            total += self.calcular_distancia(cidade_a, cidade_b)

        cidade_final = self.coordenadas[rota[-1]]
        cidade_inicio = self.coordenadas[rota[0]]

        total += self.calcular_distancia(cidade_final, cidade_inicio)

        return total

    # =====================================================
    # POPULAÇÃO INICIAL
    # =====================================================

    def inicializar_populacao(self):

        populacao = []

        rota_base = list(range(self.numcidades))

        for _ in range(TAM_POPULACAO):

            nova_rota = rota_base[:]

            random.shuffle(nova_rota)

            populacao.append(nova_rota)

        return populacao

    # =====================================================
    # SELEÇÃO POR TORNEIO
    # =====================================================

    def selecao_torneio(self, populacao, distancias):

        melhor_idx = random.randint(0, TAM_POPULACAO - 1)

        for _ in range(1, TAM_TORNEIO):

            idx = random.randint(0, TAM_POPULACAO - 1)

            if distancias[idx] < distancias[melhor_idx]:

                melhor_idx = idx

        return populacao[melhor_idx]

    # =====================================================
    # CROSSOVER OX
    # =====================================================

    def ordenar_crossover(self, pai1, pai2):

        numcidades = len(pai1)

        inicio = random.randint(0, numcidades - 1)
        fim = random.randint(0, numcidades - 1)

        if inicio > fim:
            inicio, fim = fim, inicio

        filho = [-1] * numcidades

        em_filho = [False] * numcidades

        # Copia trecho do pai1
        for i in range(inicio, fim + 1):

            filho[i] = pai1[i]

            em_filho[pai1[i]] = True

        # Completa com pai2
        index_atual = (fim + 1) % numcidades

        for i in range(numcidades):

            cidade_p2 = pai2[(fim + 1 + i) % numcidades]

            if not em_filho[cidade_p2]:

                filho[index_atual] = cidade_p2

                index_atual = (index_atual + 1) % numcidades

        return filho

    # =====================================================
    # MUTAÇÃO
    # =====================================================

    def mutar(self, rota):

        if random.random() < TAXA_MUTACAO:

            idx1 = random.randint(0, len(rota) - 1)
            idx2 = random.randint(0, len(rota) - 1)

            rota[idx1], rota[idx2] = rota[idx2], rota[idx1]

    # =====================================================
    # EXECUÇÃO PRINCIPAL
    # =====================================================

    def executar(self, verbose=True):

        populacao = self.inicializar_populacao()

        for geracao in range(MAX_GERACOES):

            distancias = [
                self.calcular_distancia_total(rota)
                for rota in populacao
            ]

            # =============================================
            # MELHOR SOLUÇÃO
            # =============================================

            for i in range(TAM_POPULACAO):

                if distancias[i] < self.melhor_distancia_global:

                    self.melhor_distancia_global = distancias[i]

                    self.melhor_rota_global = populacao[i][:]

            # =============================================
            # HISTÓRICO
            # =============================================

            self.historico_melhor.append(
                self.melhor_distancia_global
            )

            self.historico_medio.append(
                sum(distancias) / len(distancias)
            )

            # =============================================
            # NOVA POPULAÇÃO
            # =============================================

            nova_populacao = []

            # Elitismo
            nova_populacao.append(
                self.melhor_rota_global[:]
            )

            while len(nova_populacao) < TAM_POPULACAO:

                pai1 = self.selecao_torneio(
                    populacao,
                    distancias
                )

                pai2 = self.selecao_torneio(
                    populacao,
                    distancias
                )

                # Crossover
                if random.random() < TAXA_CROSSOVER:

                    filho = self.ordenar_crossover(
                        pai1,
                        pai2
                    )

                else:

                    filho = pai1[:]

                # Mutação
                self.mutar(filho)

                nova_populacao.append(filho)

            populacao = nova_populacao

            if verbose:

                print(
                    f"Geração {geracao+1:4d} | "
                    f"Melhor: {self.melhor_distancia_global:.2f} | "
                    f"Média: {self.historico_medio[-1]:.2f}"
                )

        return (
            self.melhor_rota_global,
            self.melhor_distancia_global
        )