# Chat via UDP

Atividade prática de Redes de Computadores sobre confirmação de entrega e reenvio em nível de aplicação.

## Arquivos

- `chat_receiver.py`: servidor/destinatário UDP na porta 5001.
- `chat_sender.py`: cliente/remetente UDP com histórico de mensagens pendentes.
- `RELATORIO.md`: relatório sucinto da implementação.
- `RELATORIO.pdf`: versão em PDF para entrega.

## Execução

Abra dois terminais na pasta dos arquivos.

Terminal 1:

```powershell
py chat_receiver.py
```

Terminal 2:

```powershell
py chat_sender.py
```

Digite mensagens no segundo terminal. Use `/status` para consultar as mensagens ainda pendentes e `/reenviar` para retransmiti-las.

O receptor descarta aleatoriamente 40% dos datagramas para simular perdas no canal. Uma mensagem só sai do dicionário de pendências quando o remetente recebe `DELIVERED|<ID>`.

## Protocolo

Mensagem enviada:

```text
MSG|<ID>|<CONTEUDO>
```

Confirmação enviada pelo receptor:

```text
DELIVERED|<ID>
```

A comunicação usa exclusivamente `socket.SOCK_DGRAM` (UDP), conforme o enunciado.
