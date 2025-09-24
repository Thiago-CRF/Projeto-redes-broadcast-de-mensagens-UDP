import socket
import json
import time

def ler_porta():
    porta_padrao = 5000

    porta = input(f"Digite a porta para escutar, ou clique enter para a porta padrão({porta_padrao}): ")
    porta = int(porta) if porta.strip() != "" else porta_padrao

    return porta

def main():
    porta = ler_porta()

#cria um socket ipv4(AF_INET) e UDP(SOCK_DGRAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#Configura pra poder reutilizar o endereço local, pra não ter risco de erro de endereço já em uso
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Associa o socket a porta escolhida e deiza aberto a todos os endereços
    sock.bind(("", porta))  # "" equivale a 0.0.0.0 (todas interfaces)
    print(f"\nEscutando broadcasts pela porta {porta} em todos os endereços. Clique Ctrl+C para sair.")

    try:
        while True:
        #recvfrom retorna (dados, (ip, porta)), fica bloqueado aqui até receber algo
            dados, endereço = sock.recvfrom(65535)  #65535 é o maximo de bytes que o pacote tem
            
            texto = dados.decode("utf-8", errors="replace")
        #tenta interpretar como JSON para converter em string, e substitiu byte invalido
            try:
            #Tenta converter string em objeto (dicionario criado antes)
                obj = json.loads(texto) 
            #pega o tempo que a mensagem foi enviada e transforma em string, se não tiver timestamp ele pega o tempo do programa
                timestamp = time.strftime("%H:%M:%S", time.localtime(obj.get("timestamp", time.time())))
            #printa a mensagem recebida com o tempo que foi enviado e endereço e numero de envio    
                print(f"[{timestamp}] recebimento #{obj.get('conta')} do endereço {endereço}: {obj.get('mensagem')}\n")
            
            except (ValueError, TypeError):
            #Imprime o texto cru se der erro de json 
                print(f"[{time.strftime('%H:%M:%S')}] recebido do endereço ({endereço}): {texto}\n")
    except KeyboardInterrupt:
        print("Interrompido pelo usuário")
    finally:
        sock.close()
        print("Socket fechado") #Fecha o socket no final após interromper, ou se houver algum erro

if __name__ == "__main__":
    main()
