# Importar bibliotecas (já importadas no exercício 1, mas repetido por clareza)
import pandas as pd
import random

# Definir a semente para resultados reproduzíveis (opcional)
random.seed(42)

# 2.1) Criar DataFrame de vendas aleatórias
num_lojas = 5
num_dias = 7
lojas = [f"Loja {i+1}" for i in range(num_lojas)]
dias = [f"Dia {i+1}" for i in range(num_dias)]

# Gerar vendas aleatórias (entre 100 e 1000 reais) para cada dia/loja
data_vendas = {}
for dia in dias:
    # Usando list comprehension para gerar números float aleatórios
    data_vendas[dia] = [random.uniform(100, 1000) for _ in range(num_lojas)]

df_vendas = pd.DataFrame(data_vendas, index=lojas)
# Arredondar os valores para duas casas decimais (valores monetários)
df_vendas = df_vendas.round(2)

print("\n### DataFrame Original de Vendas (em R$) ###")
print(df_vendas)
print("-" * 40)

# 2.2) Calcular o total de vendas por loja
# Soma de vendas por linha (axis=1)
df_vendas["Total de Vendas"] = df_vendas.sum(axis=1).round(2)

print("\n### Total de Vendas por Loja (Semanal) ###")
print(df_vendas[["Total de Vendas"]])
print("-" * 40)

# 2.3) Mostrar qual loja vendeu mais na semana
loja_mais_vendeu = df_vendas["Total de Vendas"].idxmax()
total_mais_vendeu = df_vendas.loc[loja_mais_vendeu, "Total de Vendas"]

print(f"\n### Loja que Mais Vendeu na Semana ###")
print(f"**Loja:** {loja_mais_vendeu}")
print(f"**Total:** R$ {total_mais_vendeu:,.2f}")
print("-" * 40)

# 2.4) Calcular o valor médio diário geral
# Média de todas as células de vendas (excluindo a coluna 'Total de Vendas')
# Ou seja, a média de todo o DataFrame antes de adicionar a coluna "Total de Vendas"
valor_medio_diario_geral = df_vendas[dias].stack().mean().round(2)
# Alternativa: df_vendas["Total de Vendas"].sum() / (num_lojas * num_dias)

print("\n### Valor Médio Diário Geral (Todas as Lojas/Dias) ###")
print(f"**Média:** R$ {valor_medio_diario_geral:,.2f}")