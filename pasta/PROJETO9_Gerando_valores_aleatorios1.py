import pandas as pd
import random

# Definir a semente para resultados reproduzíveis (opcional)
random.seed(42)

# Lista de nomes inventados (10 nomes)
nomes_alunos = [
    "Alice Silva",
    "Bruno Mendes",
    "Carla Ribeiro",
    "Daniel Ferreira",
    "Eva Souza",
    "Fábio Lima",
    "Giovana Santos",
    "Heitor Rocha",
    "Isabela Gomes",
    "Júlio Costa"
]
num_alunos = len(nomes_alunos) # Garante que o número de alunos é 10

materias = ["Matemática", "Português", "Ciências"]

# Geração dos dados
data_notas = {
    "Aluno": nomes_alunos, # Usando a nova lista de nomes
    "Matemática": [random.randint(0, 10) for _ in range(num_alunos)],
    "Português": [random.randint(0, 10) for _ in range(num_alunos)],
    "Ciências": [random.randint(0, 10) for _ in range(num_alunos)]
}

df_notas = pd.DataFrame(data_notas)

print("### DataFrame Original de Notas ###")
print(df_notas)
print("-" * 40)

# 1.2) Calcular a média geral de cada aluno
# A média é calculada apenas sobre as colunas das matérias
# Usando axis=1 para calcular a média por linha
df_notas["Média Geral"] = df_notas[materias].mean(axis=1).round(2)

print("\n### DataFrame com Média Geral ###")
print(df_notas)
print("-" * 40)

# 1.3) Mostrar o aluno com a maior média
# idxmax() retorna o índice da linha com o valor máximo na coluna "Média Geral"
aluno_maior_media = df_notas.loc[df_notas["Média Geral"].idxmax()]

print("\n### Aluno com a Maior Média Geral ###")
print(aluno_maior_media[["Aluno", "Média Geral"]])