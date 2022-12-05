import jpysocket
import socket
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pymongo import MongoClient

#Conversão de mm para pontos
def mm2p(milimetros):
    return milimetros/0.352777
##Definir quem é o ganhador da rodada
def checkWinner(mensagemEnvioClient, msgrecv):
    #Tesoura corta papel
    #Papel cobre pedra
    #Pedra esmaga lagarto
    #Lagarto envenena Spock
    #Spock esmaga (ou derrete) tesoura
    #Tesoura decapita lagarto
    #Lagarto come papel
    #Papel refuta Spock
    #Spock vaporiza pedra
    #Pedra amassa tesoura
    vencedor='Erro'
    if mensagemEnvioClient == 'Tesoura':
        if msgrecv=='Papel':
            vencedor= 'Cliente'
        elif msgrecv == 'Lagarto':
            vencedor= 'Cliente'
        elif msgrecv == 'Tesoura':
            vencedor = 'Empate'
        else:
            vencedor= 'Servidor'
    elif mensagemEnvioClient=='Papel':
        if msgrecv=='Pedra':
            vencedor='Cliente'
        elif msgrecv=='Spock':
            vencedor='Cliente'
        elif msgrecv == 'Papel':
            vencedor = 'Empate'
        else:
            vencedor='Servidor'
    elif mensagemEnvioClient == 'Pedra':
        if msgrecv == 'Tesoura':
            vencedor='Cliente'
        elif msgrecv == 'Lagarto':
            vencedor='Cliente'
        elif msgrecv == 'Pedra':
            vencedor = 'Empate'
        else:
            vencedor='Servidor'
    elif mensagemEnvioClient == 'Lagarto':
        if msgrecv == 'Spock':
            vencedor='Cliente'
        elif msgrecv == 'Papel':
            vencedor='Cliente'
        elif msgrecv == 'Lagarto':
            vencedor = 'Empate'
        else:
            vencedor='Servidor'
    elif mensagemEnvioClient == 'Spock':
        if msgrecv == 'Tesoura':
            vencedor='Cliente'
        elif msgrecv == 'Pedra':
            vencedor='Cliente'
        elif msgrecv == 'Spock':
            vencedor = 'Empate'
        else:
            vencedor='Servidor'       

    return vencedor
#Conexão com a base de dados
client = MongoClient("localhost", 27017)
db = client.DadosArmazenadosPython

##Conexão com o Servidor
host='localhost' #Host Name
port=12345    #Port Number
s=socket.socket() #Create Socket
s.connect((host,port)) #Connect to socket
print("Socket Is Connected....")
countClient = 0
countServer = 0
countEmpate = 0
##Criar o pdf
pdf = canvas.Canvas("boletim_pdf.pdf")
##Loop do sorteio da jogada e do envio e recebimento da mensagem
for i in range(0,15):
    #Enviar a jogada
    opcoesJogadas = ['Pedra', 'Papel', 'Tesoura', 'Lagarto', 'Spock']
    mensagemEnvioClient = random.choice(opcoesJogadas)
    msgrecv=s.recv(1024) #Recieve msg
    msgrecv=jpysocket.jpydecode(msgrecv) #Decript msg of server
    msgsend=jpysocket.jpyencode(mensagemEnvioClient) #Encript my Msg 
    s.send(msgsend) #Send Msg
    #escrever quem é o vencedor
    print(f"Rodada {i+1}: ")
    pdf.drawString(10 if i<10 else mm2p(110),mm2p(290-20*i) if i<10 else mm2p(290-20*(i-10)),f"Rodada {i+1}")
    print(f"{mensagemEnvioClient} X {msgrecv}")
    pdf.drawString(10 if i<10 else mm2p(110),mm2p(290-20*i-5) if i<10 else mm2p(290-20*(i-10)-5),f"{mensagemEnvioClient} X {msgrecv}")
    vencedor = checkWinner(mensagemEnvioClient, msgrecv)
    print(f"Vencedor: {vencedor}")
    pdf.drawString(10 if i<10 else mm2p(110),mm2p(290-20*i-10) if i<10 else mm2p(290-20*(i-10)-10),f"Vencedor: {vencedor}")
    #Contagem das vitorias
    if vencedor == "Cliente":
        countClient=countClient+1
    elif vencedor == "Servidor":
        countServer=countServer+1
    else:
        countEmpate = countEmpate + 1
    print("-----------------------------------------------------")
    pdf.drawString(10 if i<10 else mm2p(110),mm2p(290-20*i-15) if i<10 else mm2p(290-20*(i-10)-15),"-----------------------------------------------------")
    ##Inserindo na base de dados
    db.resultados.insert_one(
        {"Cliente": mensagemEnvioClient,
        "Servidor": msgrecv,
        "Vencedor": vencedor
        }
    )

##Printando quem é o vencedor final após as 15 rodadas
if countServer<countClient:
    print(f"Vencedor final foi o Cliente com {countClient} vitorias, {countEmpate} empates e {countServer} derrotas")
    pdf.drawString(mm2p(45),mm2p(75),f"Vencedor final foi o Cliente com {countClient} vitorias, {countEmpate} empates e {countServer} derrotas")

elif countServer>countClient:
    print(f"Vencedor final foi o Servidor com {countServer} vitorias, {countEmpate} empates e {countClient} derrotas")
    pdf.drawString(mm2p(45),mm2p(75),f"Vencedor final foi o Servidor com {countServer} vitorias, {countEmpate} empates e {countClient} derrotas")

elif countServer == countClient:
    print(f"Houve um empate com o Cliente tendo {countClient} vitorias, {countEmpate} empates e {countServer} derrotas")
    pdf.drawString(mm2p(45),mm2p(75),f"Houve um empate com o Cliente tendo {countClient} vitorias, {countEmpate} empates e {countServer} derrotas")

pdf.save() #pdf salvo
s.close() #Close connection
print("Connection Closed.")