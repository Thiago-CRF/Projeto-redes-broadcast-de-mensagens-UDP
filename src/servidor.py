import socket   #biblioteca pra manipular o socket UDP
import time     
import argparse #pra pegar argumentos pela linha de comando (a porta, mensagem e intervalo)
import json     #para enviar a mensagem em json

def ler_valores():
    porta_padrao = 5000
    intervalo_padrao = 2.0
    broadcast_padrao = "<broadcast>"    #endereça para a rede atual do pc, escolhida pelo SO

    porta = input(f"Digite a porta da conexão, ou clique enter para a porta padrão({porta_padrao}): ")
    porta = int(porta) if porta.strip() != "" else porta_padrao

    intervalo = input(f"Digite o intervalo de envio, ou clique enter para o intervalo padrão({intervalo_padrao} s): ")
    intervalo = float(intervalo) if intervalo.strip() != "" else intervalo_padrao

    mensagem = input("Digite a mensagem para broadcast: ")

    broadcast = input(f"Digite o endereço de broadcast, ou clique enter para o endereço padrão({broadcast_padrao}): ")
    broadcast = broadcast if broadcast.strip() != "" else broadcast_padrao

    return porta, intervalo, mensagem, broadcast

def main():
    porta, intervalo, mensagem, broadcast = ler_valores()

    print(f"Iniciando servidor de broadcast. Com a mensagem: '{mensagem}'")
    print(f"Porta: {porta}, broadcast: {broadcast}, intervalo: {intervalo}")
    print("Clique Ctrl+C para interromper o envio")

#cria um socket ipv4(AF_INET) e UDP(SOCK_DGRAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#Configura o socket para envio de broadcast
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#Configura pra poder reutilizar o endereço local, pra não ter risco de erro de endereço já em uso
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    conta = 0

    



if __name__ == "__main__":
    main()