import sqlite3
import csv

# Conecta-se à base de dados SQLite
conn = sqlite3.connect('mensagem1.db')
c = conn.cursor()

# Lê os dados da tabela de mensagens
c.execute("SELECT * FROM mensagens")
dados = c.fetchall()

# Escreve os dados em um arquivo CSV
with open('mensagens.csv', 'w', newline='') as arquivo_csv:
    escritor_csv = csv.writer(arquivo_csv)
    # Escreve o cabeçalho do CSV
    escritor_csv.writerow(['timestamp', 'data_hex', 'arbitration_id'])
    # Escreve os dados das mensagens
    escritor_csv.writerows(dados)

print("Dados transcritos para o arquivo CSV 'mensagens.csv'.")
