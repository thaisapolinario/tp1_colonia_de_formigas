import matplotlib.pyplot as plt
 
 
def plotar_convergencia(historico_melhor, historico_medio, salvar_como="convergencia_aco.png"):

    fig, ax = plt.subplots(figsize=(9, 4))
 
    ax.plot(historico_melhor, label="Melhor distância", linewidth=2, color="#1a6faf")
    ax.plot(historico_medio,  label="Distância média",  linewidth=1,
            color="#aac4de", linestyle="--")
 
    ax.set_xlabel("Iteração")
    ax.set_ylabel("Distância total")
    ax.set_title("Convergência — Colônia de Formigas (ACO)")
    ax.legend()
    ax.grid(True, linewidth=0.4, alpha=0.6)
 
    plt.tight_layout()
    plt.savefig(salvar_como, dpi=150)
    print(f"Gráfico de convergência salvo em: {salvar_como}")
    plt.show()
 
 
def plotar_rota(coordenadas, caminho, distancia, salvar_como="rota_aco.png"):

    fig, ax = plt.subplots(figsize=(7, 6))
 
    xs = [c[0] for c in coordenadas]
    ys = [c[1] for c in coordenadas]
    ax.scatter(xs, ys, s=60, color="#1a6faf", zorder=3)
 
    for i, (x, y) in enumerate(coordenadas):
        ax.annotate(str(i + 1), (x, y),
                    textcoords="offset points", xytext=(6, 4), fontsize=8)
 
    rota_fechada = caminho + [caminho[0]]
    for i in range(len(rota_fechada) - 1):
        a = coordenadas[rota_fechada[i]]
        b = coordenadas[rota_fechada[i + 1]]
        ax.annotate("", xy=b, xytext=a,
                    arrowprops=dict(arrowstyle="->", color="#e05c2a",
                                   lw=1.2, shrinkA=5, shrinkB=5))
 
    ax.set_title(f"Melhor rota encontrada — distância: {distancia:.2f}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, linewidth=0.4, alpha=0.5)
 
    plt.tight_layout()
    plt.savefig(salvar_como, dpi=150)
    print(f"Gráfico de rota salvo em: {salvar_como}")
    plt.show()
 