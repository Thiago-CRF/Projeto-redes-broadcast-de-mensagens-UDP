"""
server.py - UDP broadcast server simples
Uso:
    python server.py --port 5000 --interval 2 --message "Olá, rede!"
"""
import socket
import time
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="UDP broadcast server")
    parser.add_argument("--port", type=int, default=5000, help="porta de destino (padrão 5000)")
    parser.add_argument("--interval", type=float, default=2.0, help="intervalo entre mensagens em segundos")
    parser.add_argument("--message", type=str, default="Mensagem de broadcast", help="texto da mensagem")
    parser.add_argument("--broadcast", type=str, default="<broadcast>",
                        help="endereço de broadcast (padrão '<broadcast>' que usa o broadcast do SO)")
    args = parser.parse_args()

    # 1) Cria socket UDP IPv4
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2) Habilita envio de broadcast
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # 3) Opcional: permite reutilizar o endereço local rapidamente (útil em desenvolvimento)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    seq = 0
    try:
        print(f"Servidor de broadcast iniciando. Enviando para {args.broadcast} porta:{args.port} a cada {args.interval}s")
        while True:
            # Monta um payload simples em JSON (ajuda leitura e depuração)
            payload = {
                "seq": seq,
                "timestamp": time.time(),
                "message": args.message
            }
            data = json.dumps(payload).encode("utf-8")  # UDP carrega bytes
            # Envia para o endereço de broadcast e porta
            sock.sendto(data, (args.broadcast, args.port))
            print(f"[enviado] seq = {seq} -> {args.broadcast} porta:{args.port}")
            seq += 1
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário (Ctrl+C)")
    finally:
        sock.close()
        print("Socket fechado.")

if __name__ == "__main__":
    main()
