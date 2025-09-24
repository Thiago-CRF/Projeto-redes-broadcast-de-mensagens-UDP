import socket   #biblioteca pra manipular o socket UDP
import time     
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

    print(f"\nIniciando servidor de broadcast. Com a mensagem: '{mensagem}'")
    print(f"Porta: {porta}, broadcast: {broadcast}, intervalo: {intervalo}")
    print("Clique Ctrl+C para interromper o envio\n")

#cria um socket ipv4(AF_INET) e UDP(SOCK_DGRAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#Configura o socket para envio de broadcast
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#Configura pra poder reutilizar o endereço local, pra não ter risco de erro de endereço já em uso
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    conta = 0
    try:
        while True:
            payload={ #cria uma estrutura dicionario pra enviar 
                "conta": conta,
                "timestamp": time.time(),
                "mensagem": mensagem
            }
        #cria uma variavel dos dados enviados, transformando o payload em json pra ser enviado pelo UDP
            dados = json.dumps(payload).encode("utf-8") 
        #envia com sendto() para o endereço e portas definidas antes
            sock.sendto(dados, (broadcast, porta))
            print(f"Enviado. Envio #{conta} -> Porta: {porta}, endereço: {broadcast}\n")  #printa pra confirmar que enviou
            conta += 1
            time.sleep(intervalo)   #espera para voltar o loop pelo tempo de intervalo

    except KeyboardInterrupt:   #condição de interromper o try
        print("Broadcast interrompido pelo usuario")
    finally:
        sock.close()
        print("Socket fechado") #fecha o socket no final após interromper, ou se houver algum erro 

    
if __name__ == "__main__":
    main()