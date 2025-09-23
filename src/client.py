import socket
import argparse
import json
import time

def main():
    parser = argparse.ArgumentParser(description="UDP broadcast listener")
    parser.add_argument("--port", type=int, default=5000, help="porta para escutar (padrão 5000)")
    args = parser.parse_args()

    # 1) Cria socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2) Permite reutilizar o endereÇo (útil em alguns SOs)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 3) Faz bind em todas interfaces na porta desejada
    sock.bind(("", args.port))  # "" equivale a 0.0.0.0 (todas interfaces)
    print(f"Escutando broadcasts na porta {args.port} (todas interfaces). Pressione Ctrl+C para sair.")

    try:
        while True:
            # recvfrom retorna (dados, (ip, port))
            data, addr = sock.recvfrom(65535)  # 65535 é o teto prático para UDP
            text = data.decode("utf-8", errors="replace")
            # tenta interpretar como JSON para exibir campos estruturados
            try:
                obj = json.loads(text)
                ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(obj.get("timestamp", time.time())))
                print(f"[{ts}] recebido de {addr}: seq={obj.get('seq')} msg={obj.get('message')}")
            except (ValueError, TypeError):
                # se não for JSON, só imprime o texto cru
                print(f"[{time.strftime('%H:%M:%S')}] recebido de {addr}: {text}")
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
