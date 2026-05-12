import numpy as np
import random
import math
import os
 

def ler_arquivo (caminho_arquivo: str):
 
    with open(caminho_arquivo, "r") as f:
      linhas = [l.strip() for l in f if l.strip ()] # strip remove espaçoes em branco
    
    num_cidades = int(linhas[0]) # o numero de cidade é a primeira linha do arquivo
    coordenadas = []

    for i in range(1, num_cidades + 1):
      partes = linhas[i].split()
      coordenadas.append((int(partes[0]), int(partes[1]))) #coordenadas X e Y

    return coordenadas


def distancia_euclidiana(cidade_um, cidade_dois):
    calculo = math.sqrt ((cidade_um[0] - cidade_dois[0])**2 + (cidade_um[1] - cidade_dois[1]) **2)

    return calculo
    

def matriz_distancias (coordenadas):
    n = len (coordenadas)
    matriz = np.zeros((n,n))

    for i in range(n):
        for j in range(n):
            if i != j:
                matriz[i][j] = distancia_euclidiana(coordenadas[i], coordenadas[j])
        
    return matriz


class ColoniaFormigas:
    # =========================================================
    # HIPERPARÂMETROS - CONFIGURAÇÃO FORTE
    # =========================================================
    # def __init__ (self, coordenadas, num_formigas = 8, num_iteracoes = 50, alfa = 0.8, beta = 1.2, evaporacao = 0.7, Q = 30.0):

    # =========================================================
    # HIPERPARÂMETROS - CONFIGURAÇÃO FORTE
    # =========================================================
    def __init__ (self, coordenadas, num_formigas = 15, num_iteracoes = 120, alfa = 1.0, beta = 1.8, evaporacao = 0.45, Q = 70.0):

        self.coordenadas = coordenadas
        self.num_cidades = len (coordenadas)
        self.num_formigas = num_formigas
        self.num_iteracoes = num_iteracoes
        self.alfa = alfa
        self.beta= beta
        self.evaporacao = evaporacao
        self.Q = Q

        self.distancias = matriz_distancias(coordenadas)

        with np.errstate(divide="ignore", invalid="ignore"):  
            self.visibilidade = np.where( self.distancias > 0, 1.0 / self.distancias, 0.0) # diagonal


        self.feromonios = np.ones((self.num_cidades, self.num_cidades)) # todos os caminhos tem o mesmo valor (1)

        self.melhor_caminho = None
        self.melhor_distancia = float ("inf")
        self.historico_melhor = [] # melhor distancia acumulada
        self.historico_medio = []


    def calcular_distancia(self,caminho): # path
        total = 0.0
        n = len(caminho)

        for i in range(n):
            origem  = caminho[i]
            destino = caminho[(i + 1) % n]
            total  += self.distancias[origem][destino]

        return total


    def proxima_cidade(self, cidade_atual, visitadas):

        candidatas = [c for c in range(self.num_cidades) if c not in visitadas] # apenas as cidades que ainda nao foram visitadas
        if not candidatas:
            return None
 
        pesos = []
        for c in candidatas:
            # formula do AOC
            tau  = self.feromonios[cidade_atual][c] ** self.alfa 
            eta  = self.visibilidade[cidade_atual][c] ** self.beta
            pesos.append(tau * eta)
 
        soma = sum(pesos)
        if soma == 0:
            pesos = [1.0 / len(candidatas)] * len(candidatas)
        else:
            pesos = [p / soma for p in pesos]
 
        return random.choices(candidatas, weights=pesos, k=1)[0]

    def construir_caminho(self):
        inicio    = random.randint(0, self.num_cidades - 1) 
        caminho   = [inicio]
        visitadas = {inicio}
 
        while len(caminho) < self.num_cidades:
            proxima = self.proxima_cidade(caminho[-1], visitadas)
            if proxima is None:
                break
            caminho.append(proxima)
            visitadas.add(proxima)
 
        return caminho
    
    def _atualizar_feromonios(self, solucoes):
        
        self.feromonios *= (1.0 - self.evaporacao)
 
    
        for caminho, distancia in solucoes:
            deposicao = self.Q / distancia
            for i in range(len(caminho)):
                origem  = caminho[i]
                destino = caminho[(i + 1) % len(caminho)]
                self.feromonios[origem][destino] += deposicao
                self.feromonios[destino][origem] += deposicao  


    def executar(self, verbose=True):
        for iteracao in range(1, self.num_iteracoes + 1):
            solucoes = []

 
            for _ in range(self.num_formigas):
                caminho   = self.construir_caminho()
                distancia = self.calcular_distancia(caminho)
                solucoes.append((caminho, distancia))
 
                if distancia < self.melhor_distancia:
                    self.melhor_distancia = distancia
                    self.melhor_caminho   = caminho[:]
 
            self._atualizar_feromonios(solucoes)
 
            distancias_interacoes = [d for _, d in solucoes]
            self.historico_melhor.append(self.melhor_distancia)
            self.historico_medio.append(sum(distancias_interacoes) / len(distancias_interacoes))
 
            if verbose:
                print(f"Iteração {iteracao:4d} | "
                      f"Melhor: {self.melhor_distancia:8.2f} | "
                      f"Média:  {self.historico_medio[-1]:8.2f}")
                
                
        return self.melhor_caminho, self.melhor_distancia