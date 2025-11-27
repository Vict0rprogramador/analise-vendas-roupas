# %%
import pandas as pd
import matplotlib.pyplot as plt
import os

plt.style.use('seaborn-v0_8-whitegrid')

try:
    pasta_destino = "Vendas Anuais de tamanhos"

    coluna_tamanho = 'Tamanho' 

    anos = ['2023', '2024', '2025']
    meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                   'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

    mapa_cores_tamanho = {
        'PP': '#d62728',
        'P':  '#ff7f0e',
        'M':  '#2ca02c',
        'G':  '#1f77b4',
        'GG': '#9467bd',
        'XG': '#8c564b',
        'XGG': '#e377c2',
        'U': '#7f7f7f'
    }
    cor_padrao = '#bcbd22'

    vencedores_anuais = []

    for ano in anos:
        df = pd.read_excel("vendas-roupas.xlsx", sheet_name=ano)
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
        df['Mes'] = df['Data'].dt.month
        
        vendas_tam = df.groupby(['Mes', coluna_tamanho])['Quantidade Vendida'].sum().reset_index()
        idx_vencedores = vendas_tam.groupby('Mes')['Quantidade Vendida'].idxmax()
        top_tamanhos = vendas_tam.loc[idx_vencedores].set_index('Mes')
        top_tamanhos = top_tamanhos.reindex(range(1, 13))

        total_por_tamanho = df.groupby(coluna_tamanho)['Quantidade Vendida'].sum()
        tamanho_campeao = total_por_tamanho.idxmax()
        qtd_campeao = total_por_tamanho.max()

        vencedores_anuais.append({
            'Ano': ano,
            'Tamanho': tamanho_campeao,
            'Quantidade': qtd_campeao
        })

        plt.figure(figsize=(12, 6))
        quantidades = top_tamanhos['Quantidade Vendida'].fillna(0)
        nomes_vencedores = top_tamanhos[coluna_tamanho].fillna('-')
        cores_barras = [mapa_cores_tamanho.get(tam, cor_padrao) for tam in nomes_vencedores]

        barras = plt.bar(
            range(1, 13), 
            quantidades, 
            color=cores_barras,
            alpha=0.8,
            edgecolor='black',
            linewidth=0.5
        )

        plt.title(f"Tamanho Mais Vendido por Mês - {ano}", fontsize=16, fontweight='bold')
        plt.xlabel("Mês", fontsize=12)
        plt.ylabel("Quantidade Vendida (Do Tamanho Vencedor)", fontsize=12)
        plt.xticks(range(1, 13), meses_nomes)
        plt.grid(axis='y', linestyle='--', alpha=0.5)

        max_y = quantidades.max()
        plt.ylim(0, max_y * 1.25)

        for i, barra in enumerate(barras):
            mes = i + 1
            if mes in top_tamanhos.index and quantidades[mes] > 0:
                tam = top_tamanhos.loc[mes, coluna_tamanho]
                qtd = top_tamanhos.loc[mes, 'Quantidade Vendida']
                
                plt.text(
                    barra.get_x() + barra.get_width() / 2,
                    barra.get_height() + (max_y * 0.02),
                    f"{tam}\n({int(qtd)})",
                    ha='center', 
                    va='bottom', 
                    fontsize=10, 
                    fontweight='bold',
                    color='black'
                )
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
            print("pasta criada")

        caminho_arquivo = os.path.join(pasta_destino, f"tamanho_mais_vendido_por_mes_{ano}.jpg")
        plt.savefig(caminho_arquivo, bbox_inches="tight")
        plt.close()

        plt.figure(figsize=(10, 6))

    anos_labels = [d['Ano'] for d in vencedores_anuais]
    qtds_anuais = [d['Quantidade'] for d in vencedores_anuais]
    tams_anuais = [d['Tamanho'] for d in vencedores_anuais]
    

    cores_anuais = [mapa_cores_tamanho.get(t, cor_padrao) for t in tams_anuais]

    barras_resumo = plt.bar(anos_labels, qtds_anuais, color=cores_anuais, edgecolor='black', width=0.5)

    plt.title("Tamanho Mais Vendido de Cada Ano (2023 - 2025)", fontsize=16, fontweight='bold')
    plt.ylabel("Quantidade Total Vendida", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    max_val_anual = max(qtds_anuais)
    plt.ylim(0, max_val_anual * 1.2)

    for i, bar in enumerate(barras_resumo):
        tam_nome = tams_anuais[i]
        qtd = qtds_anuais[i]
        
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + (max_val_anual * 0.02),
            f"Vencedor: {tam_nome}\n({int(qtd)} vendas)",
            ha='center', va='bottom', fontsize=12, fontweight='bold'
        )
    caminho_arquivo = os.path.join(pasta_destino, "resumo_tamanho_mais_vendido_2023_2025.jpg")
    plt.savefig(caminho_arquivo, bbox_inches="tight")
    plt.close()

except Exception as e:
    print(f"Ocorreu um erro: {e}")
    # %%