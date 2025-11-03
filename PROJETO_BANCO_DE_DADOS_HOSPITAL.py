import sqlite3

hospital = sqlite3.connect('hospital.db')

cursor = hospital.cursor()

# cursor.execute("SELECT nome FROM pacientes WHERE cidade = 'São Paulo'")
# cursor.execute("SELECT nome,diagnostico FROM pacientes WHERE idade > 39")
# cursor.execute("SELECT nome,plano_saude FROM pacientes WHERE plano_saude = 'Unimed'")
# cursor.execute("SELECT nome,data_internacao FROM pacientes ORDER BY data_internacao ASC")
# cursor.execute("SELECT nome FROM pacientes WHERE diagnostico = 'Fratura'")
# cursor.execute("SELECT nome FROM pacientes WHERE medico_responsavel = 'Dr. João'")

print('--------------------------------------------------------------------------------------------------------------')
print(cursor.fetchall())
print('--------------------------------------------------------------------------------------------------------------')