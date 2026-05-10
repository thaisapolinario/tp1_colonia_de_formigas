#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <random>
#include <numeric>

using namespace std;

// Estrutura para armazenar as coordenadas de uma cidade
struct Cidade {
    double x, y;
};

// Hiperparâmetros
const int TAM_POPULACAO = 100;
const int MAX_GERACOES = 1000;
const double TAXA_MUTACAO = 0.05;
const double TAXA_CROSSOVER = 0.90;
const int TAM_TORNEIO = 3;

// Função para calcular a distância Euclidiana entre duas cidades
double calcular_distancia(Cidade a, Cidade b) {
    return sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2));
}

// Calcula a distância total de uma rota
double calcular_distancia_total(const vector<int>& rota, const vector<Cidade>& cidades) {
    double totalDist = 0;
    for (size_t i = 0; i < rota.size() - 1; ++i) {
        totalDist += calcular_distancia(cidades[rota[i]], cidades[rota[i+1]]);
    }
    // Retorna à cidade de origem
    totalDist += calcular_distancia(cidades[rota.back()], cidades[rota.front()]);
    return totalDist;
}

// Inicializa a população aleatoriamente
vector<vector<int>> inicializar_populacao(int numcidades, mt19937& rng) {
    vector<vector<int>> populacao(TAM_POPULACAO, vector<int>(numcidades));
    vector<int> rota_base(numcidades);
    iota(rota_base.begin(), rota_base.end(), 0); 

    for (int i = 0; i < TAM_POPULACAO; ++i) {
        populacao[i] = rota_base;
        shuffle(populacao[i].begin(), populacao[i].end(), rng);
    }
    return populacao;
}

// Seleção por Torneio
vector<int> selecao_torneio(const vector<vector<int>>& populacao, const vector<double>& fitnesses, mt19937& rng) {
    uniform_int_distribution<int> dist(0, TAM_POPULACAO - 1);
    int melhor_Idx = dist(rng);
    
    for (int i = 1; i < TAM_TORNEIO; ++i) {
        int idx = dist(rng);
        if (fitnesses[idx] < fitnesses[melhor_Idx]) { // Menor distância = melhor fitness
            melhor_Idx = idx;
        }
    }
    return populacao[melhor_Idx];
}

// Crossover Ordenado (OX)
vector<int> ordenar_crossover(const vector<int>& pai1, const vector<int>& pai2, mt19937& rng) {
    int numcidades = pai1.size();
    uniform_int_distribution<int> dist(0, numcidades - 1);
    
    int inicio = dist(rng);
    int fim = dist(rng);
    if (inicio > fim) swap(inicio, fim);

    vector<int> filho(numcidades, -1);
    vector<bool> em_filho(numcidades, false);

    // Copia um trecho do Pai 1
    for (int i = inicio; i <= fim; ++i) {
        filho[i] = pai1[i];
        em_filho[pai1[i]] = true;
    }

    // Preenche o resto com o Pai 2
    int index_atual = (fim + 1) % numcidades;
    for (int i = 0; i < numcidades; ++i) {
        int p2Cidade = pai2[(fim + 1 + i) % numcidades];
        if (!em_filho[p2Cidade]) {
            filho[index_atual] = p2Cidade;
            index_atual = (index_atual + 1) % numcidades;
        }
    }
    return filho;
}

// Mutação por Troca (Swap)
void mutar(vector<int>& rota, mt19937& rng) {
    uniform_real_distribution<double> probDist(0.0, 1.0);
    if (probDist(rng) < TAXA_MUTACAO) {
        uniform_int_distribution<int> idxDist(0, rota.size() - 1);
        int idx1 = idxDist(rng);
        int idx2 = idxDist(rng);
        swap(rota[idx1], rota[idx2]);
    }
}

int main() {
    int numcidades;
    if (!(cin >> numcidades)) return 0; // Lê a primeira linha: número de cidades

    vector<Cidade> cidades(numcidades);
    for (int i = 0; i < numcidades; ++i) {
        cin >> cidades[i].x >> cidades[i].y; // Lê as coordenadas x e y
    }

    random_device rd;
    mt19937 rng(rd());

    vector<vector<int>> populacao = inicializar_populacao(numcidades, rng);
    
    double melhor_distancia_global = numeric_limits<double>::max();
    vector<int> melhor_rota_global;

    for (int generation = 0; generation < MAX_GERACOES; ++generation) {
        vector<double> distancias(TAM_POPULACAO);
        
        // Avaliação
        for (int i = 0; i < TAM_POPULACAO; ++i) {
            distancias[i] = calcular_distancia_total(populacao[i], cidades);
            if (distancias[i] < melhor_distancia_global) {
                melhor_distancia_global = distancias[i];
                melhor_rota_global = populacao[i];
            }
        }

        vector<vector<int>> nova_populacao;
        
        // Elitismo: mantém o melhor da geração
        nova_populacao.push_back(melhor_rota_global);

        // Gera o restante da população
        uniform_real_distribution<double> probDist(0.0, 1.0);
        while (nova_populacao.size() < TAM_POPULACAO) {
            vector<int> pai1 = selecao_torneio(populacao, distancias, rng);
            vector<int> pai2 = selecao_torneio(populacao, distancias, rng);
            
            vector<int> filho;
            if (probDist(rng) < TAXA_CROSSOVER) {
                filho = ordenar_crossover(pai1, pai2, rng);
            } else {
                filho = pai1;
            }

            mutar(filho, rng);
            nova_populacao.push_back(filho);
        }

        populacao = nova_populacao;
    }

    cout << "Melhor Distancia Encontrada: " << melhor_distancia_global << endl;
    cout << "Rota: ";
    for (int CidadeIdx : melhor_rota_global) {
        cout << CidadeIdx << " -> ";
    }
    cout << melhor_rota_global.front() << " (Retorno)" << endl;

    return 0;
}
