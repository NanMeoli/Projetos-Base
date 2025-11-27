# Importar bibliotecas (já importadas no exercício 1, mas repetido por clareza)
import pandas as pd
import random

# Definir a semente para resultados reproduzíveis (opcional)
random.seed(42)

# 4.1) Criar DataFrame de 50 lançamentos de dado
num_lancamentos = 50

# Geração dos resultados (inteiros de 1 a 6)
resultados = [random.randint(1, 6) for _ in range(num_lancamentos)]

df_dados = pd.DataFrame({"Lançamento": range(1, num_lancamentos + 1), "Resultado": resultados})

print("\n### Primeiros 10 Lançamentos de Dados ###")
# Mostra apenas os 10 primeiros
print(df_dados.head(10))
print("-" * 40)

# 4.2) Mostre quantas vezes cada número foi sorteado
contagem_resultados = df_dados["Resultado"].value_counts().sort_index()

print("\n### Contagem de Vezes que Cada Número Foi Sorteado ###")
print(contagem_resultados)
print("-" * 40)

# 4.3) Crie uma coluna adicional chamada "Par/Ímpar"
# Usando np.where ou aplicação de função lambda
df_dados["Par/Ímpar"] = df_dados["Resultado"].apply(lambda x: "Par" if x % 2 == 0 else "Ímpar")

print("\n### Primeiros 10 Lançamentos com Categoria Par/Ímpar ###")
print(df_dados.head(10))
print("-" * 40)

# 4.4) Mostre quantas vezes saíram números pares e ímpares
contagem_par_impar = df_dados["Par/Ímpar"].value_counts()

print("\n### Contagem de Resultados Pares e Ímpares ###")
print(contagem_par_impar)