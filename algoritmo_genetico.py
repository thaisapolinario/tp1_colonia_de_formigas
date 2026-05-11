import math
import random
import sys

# Estrutura para armazenar as coordenadas de uma cidade
class Cidade:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Hiperparâmetros
TAM_POPULACAO = 100
MAX_GERACOES = 1000
TAXA_MUTACAO = 0.05
TAXA_CROSSOVER = 0.90
TAM_TORNEIO = 3

# Função para calcular a distância Euclidiana entre duas cidades
def calcular_distancia(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

# Calcula a distância total de uma rota
def calcular_distancia_total(rota, cidades):
    total_dist = 0.0
    for i in range(len(rota) - 1):
        total_dist += calcular_distancia(cidades[rota[i]], cidades[rota[i+1]])
    # Retorna à cidade de origem
    total_dist += calcular_distancia(cidades[rota[-1]], cidades[rota[0]])
    return total_dist

# Inicializa a população aleatoriamente
def inicializar_populacao(numcidades):
    populacao = []
    rota_base = list(range(numcidades))
    
    for _ in range(TAM_POPULACAO):
        nova_rota = rota_base[:] # Cria uma cópia da rota base
        random.shuffle(nova_rota)
        populacao.append(nova_rota)
        
    return populacao

# Seleção por Torneio
def selecao_torneio(populacao, distancias):
    melhor_idx = random.randint(0, TAM_POPULACAO - 1)
    
    for _ in range(1, TAM_TORNEIO):
        idx = random.randint(0, TAM_POPULACAO - 1)
        if distancias[idx] < distancias[melhor_idx]: # Menor distância = melhor fitness
            melhor_idx = idx
            
    return populacao[melhor_idx]

# Crossover Ordenado (OX)
def ordenar_crossover(pai1, pai2):
    numcidades = len(pai1)
    
    inicio = random.randint(0, numcidades - 1)
    fim = random.randint(0, numcidades - 1)
    if inicio > fim:
        inicio, fim = fim, inicio

    filho = [-1] * numcidades
    em_filho = [False] * numcidades

    # Copia um trecho do Pai 1
    for i in range(inicio, fim + 1):
        filho[i] = pai1[i]
        em_filho[pai1[i]] = True

    # Preenche o resto com o Pai 2
    index_atual = (fim + 1) % numcidades
    for i in range(numcidades):
        p2Cidade = pai2[(fim + 1 + i) % numcidades]
        if not em_filho[p2Cidade]:
            filho[index_atual] = p2Cidade
            index_atual = (index_atual + 1) % numcidades
            
    return filho

# Mutação por Troca (Swap)
def mutar(rota):
    if random.random() < TAXA_MUTACAO:
        idx1 = random.randint(0, len(rota) - 1)
        idx2 = random.randint(0, len(rota) - 1)
        # Troca os elementos de posição de forma pythonica
        rota[idx1], rota[idx2] = rota[idx2], rota[idx1]

def main():
    # Lê toda a entrada padrão de uma vez e divide em tokens (espaços/quebras de linha)
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    numcidades = int(input_data[0])
    cidades = []
    
    idx = 1
    for _ in range(numcidades):
        cidades.append(Cidade(float(input_data[idx]), float(input_data[idx+1])))
        idx += 2

    populacao = inicializar_populacao(numcidades)
    
    melhor_distancia_global = float('inf')
    melhor_rota_global = []

    for generation in range(MAX_GERACOES):
        distancias = [calcular_distancia_total(rota, cidades) for rota in populacao]
        
        # Avaliação
        for i in range(TAM_POPULACAO):
            if distancias[i] < melhor_distancia_global:
                melhor_distancia_global = distancias[i]
                melhor_rota_global = populacao[i][:] # Salva uma cópia da melhor rota

        nova_populacao = []
        
        # Elitismo: mantém o melhor da geração
        nova_populacao.append(melhor_rota_global[:])

        # Gera o restante da população
        while len(nova_populacao) < TAM_POPULACAO:
            pai1 = selecao_torneio(populacao, distancias)
            pai2 = selecao_torneio(populacao, distancias)
            
            if random.random() < TAXA_CROSSOVER:
                filho = ordenar_crossover(pai1, pai2)
            else:
                filho = pai1[:] # Cópia do pai1

            mutar(filho)
            nova_populacao.append(filho)

        populacao = nova_populacao

    print(f"Melhor Distancia Encontrada: {melhor_distancia_global}")
    
    # Formata a rota para impressão
    rota_str = " -> ".join(map(str, melhor_rota_global))
    print(f"Rota: {rota_str} -> {melhor_rota_global[0]} (Retorno)")

if __name__ == "__main__":
    main()
