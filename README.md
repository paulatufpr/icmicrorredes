Git dedicado ao desenvolvimento do metodo de leitura para os equipamentos que comunicam via CAN no laboratorio de microrredes.
O desenvolvimento sera dividido em duas frentes: python para ser usado enquanto a solucao no MOXA nao esta pronta e C caso seja possivel usar o moxa para controle dos BMS.

À utilização dos scripts feitos:

######################################################################################################################################################################
  
  ######################################################################################################################################################################
  


leitor_BMS está bem comentado, apenas o que falta para implementação é o ajuste ao inves de usar o socketCAN o programa será rodado em uma maquina windows o que envolve mudar os parametros na variavel b1(channel e interface) além da instalação de drivers compatíveis com os leitores CAN do laborátório.

  Mais sobre esses drivers e parametros na documentação do python-can(recomendo tentativa de uso do peak-can pois temos esse no laboratório e os drivers são oficiais diferentemente da gambiarra que é necessária para usar o CANdapter: https://python-can.readthedocs.io/en/stable/interfaces.html
  
  É importante que o servidor TCP do CLP esteja ligado quando o código for rodar, caso contrário o próprio python irá considerar um erro no codigo no qual a conexão do socket não foi estabelecida, caso queiram contornar esse problema basta realizar expressões de try/error.
  
  O tempo de sleep deve ser ajustado de acordo com a necessidade do CLP e deve ser feita a configuração dos métodos que seram utilizados na variável mensagem.
  Segue a documentação dos métodos da biblioteca python-can: https://python-can.readthedocs.io/en/stable/message.html
  
  ######################################################################################################################################################################
  
  ######################################################################################################################################################################
  
  
db_BMS roda uma instancia de uma base de dados extremamente leve que não precisa de configuração nem instalação de programas. O tempo de amostra pode ser ajustado novamente pelo sleep no loop principal. O codigo foi feito sem muito pensamento até pela falta de tempo então se possível no futuro fazer algo mais robusto.

######################################################################################################################################################################
  
  ######################################################################################################################################################################
  

transcrever_db é um script apenas para a leitura dos dados em formato CSV(facilidade de leitura no excel) para uso de quem necessitar dos dados.

######################################################################################################################################################################
  
  ######################################################################################################################################################################
  


Comentários adicionais: 
-nunca nomear qualquer codigo que envolve a biblioteca python-can com as letras "can" escritas dessa exata forma ou o codigo não rodará.

