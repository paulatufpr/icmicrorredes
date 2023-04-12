import can
import time
import socket
import sqlite3
#   Configuração do bus CAN
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



# Configuração do socket TCP
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 12345  # Porta para a conexão

def monitorar():
    m = escuta.get_message(1) # Atributo da fila para dar "fetch" na mensagem
    if m is not None:
        return m
    # M tem varios metodos porém o que mais interessa devido as configurações possíveis no perfil do bms usaremos apenas m.arbitration_id para filtrar os dados requisitados.
    #if (m.arbitration_id == 1713):     # Nesse ID e nos elementos 4 e 5 temos uma informação de temperatura no perfil base,  o formato vem em bytearray.
    #    temperatura1 = m.data[4]
    #    temperatura2 = m.data[5]
    #    return temperatura1, temperatura2

def enviar_tupla_via_tcp(msg_tuple):
    while True:
        try:
            # Cria o socket TCP
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))  # Conecta ao servidor
            msg = ",".join(str(item) for item in msg_tuple) # Converte a tupla em uma string separada por vírgulas
            s.sendall(msg.encode())  # Envia a mensagem codificada em bytes
            s.close()  # Fecha o socket
            break  # Sai do loop caso a conexão e envio sejam bem-sucedidos
        except socket.error as e:
            print(f"Erro de conexão: {e}")
            print("Tentando novamente em 1 segundo...")
            time.sleep(1)  # Espera 1 segundo antes de tentar novamente

def salvar_tupla_no_banco_de_dados(msg_tuple):
    # Insere os valores da tupla nas colunas correspondentes no banco de dados
    c.execute("INSERT INTO mensagens (timestamp, data_hex, arbitration_id) VALUES (?, ?, ?)", msg_tuple)
    conn.commit()  # Confirma a inserção dos dados

# Loop principal infinito.
while True:
    mensagem = monitorar()
    if mensagem is not None:
        msg_tuple = (mensagem.timestamp, mensagem.data.hex(), mensagem.arbitration_id) #mais metodos que foram usados para testes, podem ser alterados a qualquer momento.
        print(msg_tuple)
        salvar_tupla_no_banco_de_dados(msg_tuple)  # Salva a tupla no banco de dados
        enviar_tupla_via_tcp(msg_tuple)  # Envia a tupla via TCP
    #time.sleep(1)   # tempo arbitário 
    
