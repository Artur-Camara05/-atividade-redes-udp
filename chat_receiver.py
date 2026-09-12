import random
import socket

HOST = "0.0.0.0"
PORT = 5001
DROP_RATE = 0.4  # Simula perda de 40% dos pacotes


def run_chat_receiver():
    # Cria um socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))

        print("=" * 58)
        print(" RECEPTOR UDP - EVIDENCIA DA ATIVIDADE")
        print(f" Porta: {PORT} | Perda simulada: {DROP_RATE * 100}%")
        print(" Aguardando mensagens...")
        print("=" * 58)

        while True:
            # Aguarda uma mensagem
            data, addr = s.recvfrom(1024)

            # Simula perda de pacote
            if random.random() < DROP_RATE:
                print("\n[DESCARTE] Pacote descartado artificialmente!")
                continue

            raw_message = data.decode("utf-8")

            # Divide a mensagem: MSG|ID|CONTEUDO
            partes = raw_message.split("|", 2)

            # Verifica se é uma mensagem válida
            if len(partes) == 3 and partes[0] == "MSG":
                msg_id = partes[1]
                texto = partes[2]

                print(f"\n[RECEBIDA] ID {msg_id}: {texto}")

                # Monta confirmação de entrega
                recibo = f"DELIVERED|{msg_id}"

                # Envia confirmação ao remetente
                s.sendto(
                    recibo.encode("utf-8"),
                    addr
                )
                print(f"[ACK ENVIADO] DELIVERED|{msg_id}")


if __name__ == "__main__":
    run_chat_receiver()