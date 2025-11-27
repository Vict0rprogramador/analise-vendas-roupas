# %%
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-whitegrid')

try:


    anos = ['2023', '2024', '2025']
    meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                   'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

    mapa_cores = {
        'Vermelho': 'red',
        'Azul': 'blue',
        'Amarelo': 'gold',
        'Verde': 'green',
        'Branco': 'white',
        'Cinza': 'gray',
        'Preto': 'black',
        'Roxo': 'purple',
        'Rosa': 'pink',
        'Laranja': 'orange'
    }

    vencedores_anuais = []

    for ano in anos:
        df = pd.read_excel("vendas-roupas.xlsx", sheet_name=ano)
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
        df['Mes'] = df['Data'].dt.month

        vendas_cor = df.groupby(['Mes', 'Cor'])['Quantidade Vendida'].sum().reset_index()
        rank_cores = vendas_cor.groupby('Mes')['Quantidade Vendida'].idxmax()
        top_cores = vendas_cor.loc[rank_cores].set_index('Mes')
        top_cores = top_cores.reindex(range(1, 13))

        total_por_cor = df.groupby('Cor')['Quantidade Vendida'].sum()
        cor_campea_ano = total_por_cor.idxmax()
        qtd_campea_ano = total_por_cor.max()

        vencedores_anuais.append({
            'Ano': ano, 
            'Cor': cor_campea_ano, 
            'Quantidade': qtd_campea_ano
        })

        plt.figure(figsize=(12, 6))
        
        barras_cores = []
        bordas_cores = []
        
        for i in range(1, 13):
            if i in top_cores.index and pd.notna(top_cores.loc[i, 'Cor']):
                cor_nome = top_cores.loc[i, 'Cor']
                cor_python = mapa_cores.get(cor_nome, 'grey') 
                barras_cores.append(cor_python)
                
                if cor_python == 'white':
                    bordas_cores.append('black')
                else:
                    bordas_cores.append(cor_python) 
            else:
                barras_cores.append('white')
                bordas_cores.append('white')

        quantidades = top_cores['Quantidade Vendida'].fillna(0)

        barras = plt.bar(
            range(1, 13), 
            quantidades, 
            color=barras_cores, 
            edgecolor=bordas_cores,
            linewidth=1
        )

        plt.title(f"Cor Mais Vendida por Mês - {ano}", fontsize=16, fontweight='bold')
        plt.xlabel("Mês", fontsize=12)
        plt.ylabel("Qtd Vendida (Cor Vencedora)", fontsize=12)
        plt.xticks(range(1, 13), meses_nomes)
        plt.grid(axis='y', linestyle='--', alpha=0.5)

        for i, barra in enumerate(barras):
            mes_idx = i + 1
            if mes_idx in top_cores.index and pd.notna(top_cores.loc[mes_idx, 'Cor']):
                qtd = top_cores.loc[mes_idx, 'Quantidade Vendida']
                nome_cor = top_cores.loc[mes_idx, 'Cor']
                
                plt.text(
                    barra.get_x() + barra.get_width() / 2,
                    barra.get_height() + (quantidades.max() * 0.02),
                    f"{nome_cor}\n({int(qtd)})",
                    ha='center', va='bottom', fontsize=9, fontweight='bold'
                )

        plt.ylim(0, quantidades.max() * 1.25)


    plt.figure(figsize=(10, 6))
    
    anos_labels = [d['Ano'] for d in vencedores_anuais]
    qtds = [d['Quantidade'] for d in vencedores_anuais]
    cores_vencedoras = [d['Cor'] for d in vencedores_anuais]
    

    bar_colors_annual = [mapa_cores.get(c, 'grey') for c in cores_vencedoras]
    edge_colors_annual = ['black' if c == 'white' else c for c in bar_colors_annual]

    barras_anual = plt.bar(
        anos_labels,
        qtds,
        color=bar_colors_annual,
        edgecolor=edge_colors_annual,
        width=0.5
    )
    
    plt.title("Cor Mais Vendida de Cada Ano (2023 - 2025)", fontsize=16, fontweight='bold')
    plt.ylabel("Quantidade Total Vendida", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    

    max_val = max(qtds)
    plt.ylim(0, max_val * 1.2)

    for i, bar in enumerate(barras_anual):
        cor_nome = cores_vencedoras[i]
        qtd = qtds[i]
        
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + (max_val * 0.02),
            f"{cor_nome}\n({int(qtd)})",
            ha='center', va='bottom', fontsize=12, fontweight='bold'
        )
    plt.show()
except Exception as e:
    print(f"Ocorreu um erro: {e}")
# %%
