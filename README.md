Git dedicado ao desenvolvimento do metodo de leitura para os equipamentos que comunicam via CAN no laboratorio de microrredes.
O desenvolvimento sera dividido em duas frentes: python para ser usado enquanto a solucao no MOXA nao esta pronta e C caso seja possivel usar o moxa para controle dos BMS.

# À utilização dos scripts feitos:

## Dependencias
```bash
Python 3.10.6 (main, Nov 14 2022, 16:10:14) [GCC 11.3.0] on linux
pip install python-can
pip install sqlite3 # não precisei rodar no linux porém talvez seja um problema no windows.

#Inicialização do CAN no linux
$ modprobe vcan0
$ sudo ip link add dev vcan0 type vcan

```


## leitor_BMS
-  Está bem comentado, apenas o que falta para implementação é o ajuste ao inves de usar o socketCAN o programa será rodado em uma maquina windows o que envolve mudar os parametros na variavel 
```python
b1 = can.Bus(channel='vcan0', interface='socketcan')
```
- Além da instalação de drivers compatíveis com os leitores CAN do laborátório.

- Mais sobre esses drivers e parametros na documentação do python-can(recomendo tentativa de uso do peak-can pois temos esse no laboratório e os drivers são oficiais diferentemente da gambiarra que é necessária para usar o CANdapter): https://python-can.readthedocs.io/en/stable/interfaces.html
  
- É importante que o servidor TCP do CLP esteja ligado quando o código for rodar, caso contrário o próprio python irá considerar um erro no codigo no qual a conexão do socket não foi estabelecida, caso queiram contornar esse problema basta realizar expressões de try/error.
```bash
s.connect((HOST, PORT))  # Conecta ao servidor
ConnectionRefusedError: [Errno 111] Connection refused
```

- O tempo de sleep deve ser ajustado de acordo com a necessidade do CLP 
```python
while True:
    mensagem = monitorar()
    if mensagem is not None:
        msg_tuple = (mensagem.timestamp, mensagem.data.hex(), mensagem.arbitration_id) 
        print(msg_tuple)
        enviar_tupla_via_tcp(msg_tuple)
  --->  time.sleep(1)   # ajustar tempo
```
- Deve ser feita a configuração dos métodos que seram utilizados na variável mensagem.
```python
msg_tuple = (mensagem.timestamp, mensagem.data.hex(), mensagem.arbitration_id)
```

- Segue a documentação dos métodos da biblioteca python-can: https://python-can.readthedocs.io/en/stable/message.html
  
 
## db_BMS
- Roda uma instancia de uma base de dados extremamente leve que não precisa de configuração nem instalação de programas. O tempo de amostra pode ser ajustado novamente pelo sleep no loop principal. O codigo foi feito sem muito pensamento até pela falta de tempo então se possível no futuro fazer algo mais robusto.
  

## transcrever_DB
- É um script apenas para a leitura dos dados em formato CSV(facilidade de leitura no excel) para uso de quem necessitar dos dados.

## server
- Pode ser usado na maquina local para debugar qualquer tipo de problema com o leitor_BMS ou a comunicação mesmo.
  
  
  


## Comentários adicionais: 
- Nunca nomear qualquer codigo que envolve a biblioteca python-can com as letras "can" escritas dessa exata forma ou o codigo não rodará;
- Os endereços ip e portas devem ser alterados para os endereços adequados do laboratório;
- Lembrar que o código foi desenvolvido em ambiente linux e portanto poderão ocorrer problemas caso apenas rodem os scripts em uma maquina windows.
