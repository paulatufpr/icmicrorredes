import can
import time
import sqlite3

b1 = can.Bus(channel='vcan0', interface='socketcan') # seta as configurações do barramento CAN

escuta = can.BufferedReader() # inicia uma fila de mensagens

notifica = can.Notifier(b1, [escuta]) # notifica uma nova mensagem

# Configuração da base de dados SQLite
conn = sqlite3.connect('mensagem1.db')  # Conecta ou cria um novo arquivo de banco de dados
c = conn.cursor()  # Cria um cursor para realizar operações no banco de dados

# Cria a tabela para armazenar as mensagens com colunas separadas
c.execute('''CREATE TABLE IF NOT EXISTS mensagens
             (timestamp TEXT, data_hex TEXT, arbitration_id INTEGER)''')
conn.commit()  # Confirma a criação da tabela

def monitorar():
    m = escuta.get_message(1) # atributo da fila para dar "fetch" na mensagem
    if m is not None:
        return m

def salvar_tupla_no_banco_de_dados(msg_tuple):
    # Insere os valores da tupla nas colunas correspondentes no banco de dados
    c.execute("INSERT INTO mensagens (timestamp, data_hex, arbitration_id) VALUES (?, ?, ?)", msg_tuple)
    conn.commit()  # Confirma a inserção dos dados

while True:
    mensagem = monitorar()
    if mensagem is not None:
        msg_tuple = (mensagem.timestamp, mensagem.data.hex(), mensagem.arbitration_id)
        print(msg_tuple)
        salvar_tupla_no_banco_de_dados(msg_tuple)  # Salva a tupla no banco de dados
    time.sleep(1)
