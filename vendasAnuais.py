# %%
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-whitegrid')

try:
    anos = ['2023', '2024', '2025']
    dados_anuais = {}
    total_vendas_anuais = []

    for ano in anos:
        df = pd.read_excel("vendas-roupas.xlsx", sheet_name=ano)
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
        
        vendas = df.groupby(df['Data'].dt.month)['Quantidade Vendida'].sum()
        dados_anuais[ano] = vendas.reindex(range(1, 13), fill_value=0)
        total_vendas_anuais.append(vendas.sum())

    fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(10, 18))
    plt.subplots_adjust(hspace=0.4)

    meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                   'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    
    cores = ["#0c78c5", '#ff7f0e', '#2ca02c']

    for i, ano in enumerate(anos):
        ax = axes[i]
        dados = dados_anuais[ano]
        
        ax.plot(
            dados.index, 
            dados.values, 
            marker='o', 
            color=cores[i], 
            linewidth=2
        )
        
        ax.set_title(f"Vendas Mensais - {ano}", fontsize=14, fontweight='bold')
        ax.set_ylabel("Qtd Vendida")
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(meses_nomes)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_ylim(0, dados.max() * 1.15)

        for x, y in zip(dados.index, dados.values):
            ax.text(
                x, #mês 
                y + (dados.max() * 0.02), #Quantidade
                f"{int(y)}",
                ha='center',
                va='bottom',
                fontsize=10,
                fontweight='bold',
                color='#333333'
            )
    
        ax_total = axes[3]
        barras = ax_total.bar(
        anos, 
        total_vendas_anuais, 
        color=cores, 
        width=0.6
    )
    
    ax_total.set_title("Total de Vendas por Ano (Comparativo)", fontsize=16, fontweight='bold')
    ax_total.set_ylabel("Total Vendido")
    ax_total.grid(axis='y', linestyle='--', alpha=0.6)
    max_total = max(total_vendas_anuais)
    ax_total.set_ylim(0, max_total * 1.15)

    for barra in barras:
        altura = barra.get_height()
        ax_total.text(
            barra.get_x() + barra.get_width() / 2,
            altura + (max_total * 0.01),
            f"{int(altura)}",
            ha='center', 
            va='bottom', 
            fontsize=12, 
            fontweight='bold'
        )

    plt.show()

except Exception as e:
    print(f"Ocorreu um erro: {e}")
# %%
