import socket
import threading

TARGET_IP = "127.0.0.1"
PORT = 5001

# Guarda mensagens que ainda não foram confirmadas
pending_messages = {}

msg_counter = 1

# Evita acesso simultâneo ao dicionário
lock = threading.Lock()


def listen_receipts(sock):
    """Recebe confirmações de entrega em segundo plano."""

    while True:
        try:
            data, _ = sock.recvfrom(1024)

            raw = data.decode("utf-8")

            # Divide DELIVERED|ID
            partes = raw.split("|", 1)

            if len(partes) == 2 and partes[0] == "DELIVERED":
                msg_id = int(partes[1])

                with lock:
                    if msg_id in pending_messages:
                        texto = pending_messages.pop(msg_id)

                        print(
                            f"\n[✓✓ Entregue] "
                            f"ID {msg_id}: {texto}"
                        )

        except Exception:
            break


def run_chat_sender():
    global msg_counter

    # Cria socket UDP
    with socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    ) as s:

        # Thread para receber confirmações
        listener = threading.Thread(
            target=listen_receipts,
            args=(s,),
            daemon=True
        )

        listener.start()

        print("=== Mini-Chat UDP ===")
        print("/status -> mensagens pendentes")
        print("/reenviar -> reenviar mensagens pendentes")

        while True:
            try:
                user_input = input(
                    "\nDigite uma mensagem: "
                ).strip()

                if not user_input:
                    continue

                # Exibe mensagens pendentes
                if user_input == "/status":

                    with lock:
                        print(
                            f"\nMensagens pendentes: "
                            f"{len(pending_messages)}"
                        )

                        for msg_id, texto in pending_messages.items():
                            print(
                                f"ID {msg_id}: {texto} "
                                "[Pendente]"
                            )

                    continue

                # Reenvia mensagens pendentes
                if user_input == "/reenviar":

                    with lock:
                        mensagens = list(
                            pending_messages.items()
                        )

                    if not mensagens:
                        print(
                            "Nenhuma mensagem pendente."
                        )

                    for msg_id, texto in mensagens:

                        pacote = f"MSG|{msg_id}|{texto}"

                        s.sendto(
                            pacote.encode("utf-8"),
                            (TARGET_IP, PORT)
                        )

                        print(
                            f"[Reenviado] "
                            f"ID {msg_id}: {texto}"
                        )

                    continue

                # Salva uma nova mensagem como pendente
                current_id = msg_counter

                with lock:
                    pending_messages[current_id] = user_input

                # Cria pacote
                pacote = (
                    f"MSG|{current_id}|{user_input}"
                )

                # Envia via UDP
                s.sendto(
                    pacote.encode("utf-8"),
                    (TARGET_IP, PORT)
                )

                print(
                    f"[Pendente] "
                    f"ID {current_id}: {user_input}"
                )

                msg_counter += 1

            except KeyboardInterrupt:
                print("\nEncerrando cliente...")
                break


if __name__ == "__main__":
    run_chat_sender()