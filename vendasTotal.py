# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    df = pd.read_excel(
        "vendas-roupas.xlsx", 
        sheet_name="vendas")
    
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    

    rank_tipo = df.groupby("Tipo de Roupa")["Quantidade Vendida"].sum().sort_values(ascending=False)

    rank_tamanho = df.groupby("Tamanho")["Quantidade Vendida"].sum().sort_values(ascending=False)

    rank_cor = df.groupby("Cor")["Quantidade Vendida"].sum().sort_values(ascending=False)

    plt.style.use("seaborn-v0_8-whitegrid")

    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 18))
    plt.subplots_adjust(hspace=0.4)

    # Grafico de roupas mais vendidas
    rank_tipo.sort_values(ascending=True).plot(
        kind="barh", color="#4682B4", width=0.8, ax=axes[0]
    )
    axes[0].set_title("Tipos de Roupas Mais Vendidos", fontsize=16)
    axes[0].set_xlabel("Quantidade Vendida")

    for bar in axes[0].patches:
        axes[0].text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f"{int(bar.get_width())}",
            va="center", ha="left", fontsize=10
        )
    # Grafico de tamanho mais vendidos
    rank_tamanho.sort_values(ascending=True).plot(
        kind="barh", color="#4682B4", width=0.8, ax=axes[1])
    
    axes[1].set_title("Tamanhos Mais Vendidos", fontsize=16)
    axes[1].set_xlabel("Quantidade Vendida")
    
    for bar in axes[1].patches:
        axes[1].text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f"{int(bar.get_width())}",
            va="center", ha="left", fontsize=10
        )
    # Grafico de cores mais vendidos
    rank_cor.sort_values(ascending=True).plot(
        kind="barh", color="#4682B4", width=0.8, ax=axes[2])
    
    axes[2].set_title("Cores Mais Vendidas", fontsize=16)
    axes[2].set_xlabel("Quantidade Vendida")

    for bar in axes[2].patches:
        axes[2].text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f"{int(bar.get_width())}",
            va="center", ha="left", fontsize=10
        )
    plt.show()
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
    
# %%
