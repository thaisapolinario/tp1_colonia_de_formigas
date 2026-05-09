import colonia_formigas
import vizualizar
import numpy as np
import random
import math
import os
 

if __name__ == "__main__":
 
    ARQUIVO = "instancia.txt"
 
    if os.path.exists(ARQUIVO):
        coordenadas = colonia_formigas.ler_arquivo(ARQUIVO)


    NUM_TENTATIVAS = 10
 
    melhor_geral          = float("inf")
    melhor_caminho_geral  = None
    melhor_aco            = None
    distancias_tentativas = []
 
    print(f"Executando {NUM_TENTATIVAS} tentativas...\n")
 
    for tentativa in range(1, NUM_TENTATIVAS + 1):
        aco = colonia_formigas.ColoniaFormigas(coordenadas)
        caminho, distancia = aco.executar(verbose=False)
        distancias_tentativas.append(distancia)
 
        print(f"Tentativa {tentativa:2d} | Distância: {distancia:.4f}")
 
        if distancia < melhor_geral:
            melhor_geral         = distancia
            melhor_caminho_geral = caminho
            melhor_aco           = aco
 
    media  = sum(distancias_tentativas) / NUM_TENTATIVAS
    minimo = min(distancias_tentativas)
    maximo = max(distancias_tentativas)
 
    rota_str = " → ".join(str(c + 1) for c in melhor_caminho_geral)
    rota_str += f" → {melhor_caminho_geral[0] + 1}"
 
    print("\nResultado")
    print(f"Melhor rota     : {rota_str}")
    print(f"Melhor distância: {melhor_geral:.4f}")
    print(f"Média           : {media:.4f}")
    print(f"Mínimo / Máximo : {minimo:.4f} / {maximo:.4f}")
 
    vizualizar.plotar_convergencia(melhor_aco.historico_melhor, melhor_aco.historico_medio)
    vizualizar.plotar_rota(coordenadas, melhor_caminho_geral, melhor_geral)