import pandas as pd
import random

# Definir a semente para resultados reproduzíveis (opcional)
random.seed(42)

# Lista de nomes inventados para 8 produtos
nomes_produtos = [
    "Teclado Mecânico Pro",
    "Mouse Óptico Gamer",
    "Monitor LED 27pol",
    "Webcam HD Streamer",
    "Fone Bluetooth ANC",
    "Hub USB-C 8 Portas",
    "SSD Externo 1TB",
    "Cabo HDMI 2.1 Reforçado"
]
num_produtos = len(nomes_produtos) # Garante que o número de produtos é 8

# 3.1) Criar DataFrame de estoque
# Geração dos dados
data_estoque = {
    "Produto": nomes_produtos, # Usando a nova lista de nomes
    # Quantidade inteira entre 10 e 100
    "Quantidade": [random.randint(10, 100) for _ in range(num_produtos)],
    # Preço float entre 5.0 e 100.0 (arredondado para 2 casas)
    "Preço": [round(random.uniform(5.0, 100.0), 2) for _ in range(num_produtos)]
}

df_estoque = pd.DataFrame(data_estoque)

print("\n### DataFrame Original de Estoque ###")
print(df_estoque)
print("-" * 40)

# 3.2) Adicionar coluna "Valor Total"
# Valor Total = Quantidade * Preço
df_estoque["Valor Total"] = (df_estoque["Quantidade"] * df_estoque["Preço"]).round(2)

print("\n### DataFrame com Valor Total ###")
print(df_estoque)
print("-" * 40)

# 3.3) Descobrir qual produto tem o maior valor total
produto_maior_valor = df_estoque.loc[df_estoque["Valor Total"].idxmax()]

print("\n### Produto com o Maior Valor Total de Estoque ###")
print(produto_maior_valor[["Produto", "Valor Total"]])
print("-" * 40)

# 3.4) Mostrar apenas os produtos com valor total acima da média
media_valor_total = df_estoque["Valor Total"].mean()
print(f"\n### Média do Valor Total: R$ {media_valor_total:.2f} ###")

# Filtragem do DataFrame
produtos_acima_media = df_estoque[df_estoque["Valor Total"] > media_valor_total]

print("\n### Produtos com Valor Total Acima da Média ###")
print(produtos_acima_media)