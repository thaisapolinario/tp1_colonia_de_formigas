import os
import time
import random
import statistics
import numpy as np
import matplotlib.pyplot as plt

import colonia_formigas
import algoritmo_genetico
import vizualizar

ARQUIVO = "instancia.txt"
NUM_EXECUCOES = 100
SEED_FIXA = False

coordenadas = colonia_formigas.ler_arquivo(ARQUIVO)

resultados_aco = {
    "distancias": [],
    "tempos": [],
    "convergencias": [],
    "melhor_distancia": float("inf"),
    "melhor_caminho": None,
    "melhor_modelo": None
}

resultados_ga = {
    "distancias": [],
    "tempos": [],
    "convergencias": [],
    "melhor_distancia": float("inf"),
    "melhor_caminho": None,
    "melhor_modelo": None
}

# =========================================================
# EXECUÇÃO ACO
# =========================================================

print("\n==============================")
print("EXECUTANDO COLÔNIA DE FORMIGAS")
print("==============================\n")

for i in range(NUM_EXECUCOES):

    if SEED_FIXA:
        random.seed(i)
        np.random.seed(i)

    inicio = time.perf_counter()

    aco = colonia_formigas.ColoniaFormigas(coordenadas)

    caminho, distancia = aco.executar(verbose=False)

    fim = time.perf_counter()

    tempo_execucao = fim - inicio

    resultados_aco["distancias"].append(distancia)
    resultados_aco["tempos"].append(tempo_execucao)
    resultados_aco["convergencias"].append(aco.historico_melhor)

    if distancia < resultados_aco["melhor_distancia"]:
        resultados_aco["melhor_distancia"] = distancia
        resultados_aco["melhor_caminho"] = caminho
        resultados_aco["melhor_modelo"] = aco

    print(f"ACO Execução {i+1:3d} | "
          f"Distância: {distancia:10.2f} | "
          f"Tempo: {tempo_execucao:.4f}s")

# =========================================================
# EXECUÇÃO GA
# =========================================================

print("\n==============================")
print("EXECUTANDO ALGORITMO GENÉTICO")
print("==============================\n")

for i in range(NUM_EXECUCOES):

    if SEED_FIXA:
        random.seed(i)
        np.random.seed(i)

    inicio = time.perf_counter()

    ga = algoritmo_genetico.AlgoritmoGenetico(coordenadas)

    caminho, distancia = ga.executar(verbose=False)

    fim = time.perf_counter()

    tempo_execucao = fim - inicio

    resultados_ga["distancias"].append(distancia)
    resultados_ga["tempos"].append(tempo_execucao)
    resultados_ga["convergencias"].append(ga.historico_melhor)

    if distancia < resultados_ga["melhor_distancia"]:
        resultados_ga["melhor_distancia"] = distancia
        resultados_ga["melhor_caminho"] = caminho
        resultados_ga["melhor_modelo"] = ga

    print(f"GA  Execução {i+1:3d} | "
          f"Distância: {distancia:10.2f} | "
          f"Tempo: {tempo_execucao:.4f}s")


# =========================================================
# FUNÇÃO ESTATÍSTICA
# =========================================================

def gerar_estatisticas(nome, resultados):

    distancias = resultados["distancias"]
    tempos = resultados["tempos"]

    print("\n===================================")
    print(f"RESULTADOS - {nome}")
    print("===================================\n")

    print(f"Melhor distância : {min(distancias):.4f}")
    print(f"Pior distância   : {max(distancias):.4f}")

    print(f"Média distância  : {statistics.mean(distancias):.4f}")
    print(f"Mediana          : {statistics.median(distancias):.4f}")

    print(f"Desvio padrão    : {statistics.stdev(distancias):.4f}")
    print(f"Variância        : {statistics.variance(distancias):.4f}")

    print(f"\nTempo médio      : {statistics.mean(tempos):.4f}s")
    print(f"Tempo mínimo     : {min(tempos):.4f}s")
    print(f"Tempo máximo     : {max(tempos):.4f}s")

    print(f"Coef. variação   : "
          f"{statistics.stdev(distancias)/statistics.mean(distancias):.4f}")


# =========================================================
# EXIBIÇÃO ESTATÍSTICA
# =========================================================

gerar_estatisticas("ACO", resultados_aco)

gerar_estatisticas("GA", resultados_ga)


# =========================================================
# COMPARAÇÃO DIRETA
# =========================================================

print("\n===================================")
print("COMPARAÇÃO FINAL")
print("===================================\n")

media_aco = statistics.mean(resultados_aco["distancias"])
media_ga = statistics.mean(resultados_ga["distancias"])

tempo_aco = statistics.mean(resultados_aco["tempos"])
tempo_ga = statistics.mean(resultados_ga["tempos"])

if media_aco < media_ga:
    print("ACO teve melhor média de solução.")
else:
    print("GA teve melhor média de solução.")

if tempo_aco < tempo_ga:
    print("ACO foi mais rápido.")
else:
    print("GA foi mais rápido.")

if statistics.stdev(resultados_aco["distancias"]) < statistics.stdev(resultados_ga["distancias"]):
    print("ACO foi mais estável.")
else:
    print("GA foi mais estável.")


# =========================================================
# GRÁFICOS
# =========================================================

# gráfico mostra a evolução média da melhor distância ao longo das iterações/gerações nas 100 execuções
def plot_convergencia(resultados_aco, resultados_ga):
    
    # média das convergências (suaviza o gráfico)
    media_aco = np.mean(resultados_aco["convergencias"], axis=0)
    media_ga = np.mean(resultados_ga["convergencias"], axis=0)

    plt.figure()

    plt.plot(media_aco, label="ACO")
    plt.plot(media_ga, label="GA")

    plt.xlabel("Iterações / Gerações")
    plt.ylabel("Melhor distância")
    plt.title("Convergência dos Algoritmos")

    plt.legend()
    plt.grid()

    plt.show()

# gráfico mostra a variação das distâncias finais por execução, utilizando boxplot (avalia a estabilidade dos algoritmos)
def plot_boxplot(resultados_aco, resultados_ga):

    plt.figure()

    plt.boxplot(
        [resultados_aco["distancias"], resultados_ga["distancias"]],
        labels=["ACO", "GA"]
    )

    plt.ylabel("Distância")
    plt.title("Distribuição das Soluções")

    plt.grid()

    plt.show()

# gráfico apresenta o tempo médio de execução de cada algoritmo nas 100 execuções
def plot_tempo(resultados_aco, resultados_ga):

    medias = [
        np.mean(resultados_aco["tempos"]),
        np.mean(resultados_ga["tempos"])
    ]

    plt.figure()

    plt.bar(["ACO", "GA"], medias)

    plt.ylabel("Tempo médio (s)")
    plt.title("Tempo Médio de Execução")

    plt.grid()

    plt.show()

# gráfico mostra a distância final obtida em cada execução para ambos os algoritmoss
def plot_execucoes(resultados_aco, resultados_ga):

    plt.figure()

    plt.plot(resultados_aco["distancias"], label="ACO", alpha=0.7)
    plt.plot(resultados_ga["distancias"], label="GA", alpha=0.7)

    plt.xlabel("Execução")
    plt.ylabel("Distância")
    plt.title("Distância por Execução")

    plt.legend()
    plt.grid()

    plt.show()


plot_convergencia(resultados_aco, resultados_ga)
plot_boxplot(resultados_aco, resultados_ga)
plot_tempo(resultados_aco, resultados_ga)
plot_execucoes(resultados_aco, resultados_ga)
