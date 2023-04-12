import can
import time
import socket
#   Configuração do bus CAN
b1 = can.Bus(channel='vcan0', interface='socketcan') # seta as configurações do barramento CAN

escuta = can.BufferedReader() # inicia uma fila de mensagens

notifica = can.Notifier(b1, [escuta]) # notifica uma nova mensagem

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
    # Cria o socket TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))  # Conecta ao servidor
    msg = ",".join(str(item) for item in msg_tuple) # Converte a tupla em uma string separada por vírgulas
    s.sendall(msg.encode())  # Envia a mensagem codificada em bytes
    s.close()  # Fecha o socket


# Loop principal infinito.
while True:
    mensagem = monitorar()
    if mensagem is not None:
        msg_tuple = (mensagem.timestamp, mensagem.data.hex(), mensagem.arbitration_id) #mais metodos que foram usados para testes, podem ser alterados a qualquer momento.
        print(msg_tuple)
        enviar_tupla_via_tcp(msg_tuple)  # Envia a tupla via TCP
    time.sleep(1)   # tempo arbitário 
    
