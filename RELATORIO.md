# Relatório sucinto: Chat via UDP

## 1. Estratégia adotada

A aplicação foi dividida em um remetente (`chat_sender.py`) e um destinatário (`chat_receiver.py`). Os dois componentes usam sockets UDP (`SOCK_DGRAM`) e trocam mensagens de texto com campos separados pelo caractere `|`.

Cada mensagem recebe um identificador inteiro sequencial e é enviada no formato `MSG|<ID>|<CONTEUDO>`. Antes do envio, o remetente registra o par ID/texto em `pending_messages`. Assim, a mensagem começa no estado **Pendente (Check Cinza)**.

O destinatário escuta a porta UDP 5001. Para simular um canal não confiável, aplica `DROP_RATE = 0.4`: em cada datagrama recebido, há 40% de chance de descarte. Quando o pacote é processado, o destinatário extrai o ID e o conteúdo, imprime a mensagem e responde ao endereço de origem com `DELIVERED|<ID>`.

Uma thread separada no remetente escuta os recibos. Ao receber um recibo válido, converte o ID para inteiro, remove a entrada correspondente de `pending_messages` e exibe **Entregue (Check Azul)**. O dicionário é protegido por `threading.Lock`, pois é acessado simultaneamente pela thread de escuta e pelo loop principal.

## 2. Captura de tela 1: perda proposital

Durante a execução, o segundo terminal envia uma mensagem e mostra seu estado como `[Pendente]`. No terminal do receptor aparece `[CANAL] Pacote descartado artificialmente!`. O comando `/status` confirma que a mensagem continua pendente, pois nenhum recibo foi recebido.

**Evidência esperada:**

```text
Remetente: [Pendente] ID 1: mensagem de teste
Receptor:  [CANAL] Pacote descartado artificialmente!
/status -> Mensagens pendentes: 1
```

## 3. Captura de tela 2: reenvio e confirmação

Com a mensagem ainda pendente, o comando `/reenviar` envia novamente todos os registros do dicionário. Quando uma retransmissão chega ao receptor, ele imprime a mensagem e devolve o recibo. O remetente então remove a mensagem da lista e mostra a confirmação de entrega.

**Evidência esperada:**

```text
Remetente: [Reenviado] ID 1: mensagem de teste
Receptor:  [MSG 1] mensagem de teste
Remetente: [✓✓ Entregue] ID 1: mensagem de teste
/status -> Mensagens pendentes: 0
```

As capturas reais desses dois momentos devem acompanhar este relatório na entrega do repositório.

## 4. Aplicação x TCP

Neste exercício, a confiabilidade é construída na camada de aplicação. O programa precisa atribuir IDs, manter pendências, gerar recibos e retransmitir mensagens que não receberam confirmação. Isso permite controlar explicitamente o significado de “entregue”, mas exige código adicional e tratamento de estados.

No TCP, a camada de transporte oferece conexão, ordenação, retransmissão e confirmação de recebimento dos segmentos. A aplicação recebe um fluxo confiável de bytes sem implementar manualmente esses mecanismos. Porém, uma confirmação TCP indica que os dados chegaram ao outro endpoint TCP; ela não significa necessariamente que a aplicação destinatária exibiu ou processou a mensagem. O recibo `DELIVERED|<ID>` deste exercício representa uma confirmação semântica em nível de aplicação.

## 5. Conformidade

- Comunicação implementada exclusivamente com UDP/`SOCK_DGRAM`.
- Porta do serviço: `5001`.
- Taxa de perda simulada: `0.4`.
- Formatos `MSG|<ID>|<CONTEUDO>` e `DELIVERED|<ID>` implementados.
- IDs sequenciais, pendências, thread de recibos, `/status` e `/reenviar` implementados.