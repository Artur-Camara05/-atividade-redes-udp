from pathlib import Path

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Preformatted

BASE_DIR = Path(__file__).resolve().parent
OUTPUT = BASE_DIR / "RELATORIO.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TituloAtividade", parent=styles["Title"], alignment=TA_CENTER, fontSize=18, leading=22, spaceAfter=18))
styles.add(ParagraphStyle(name="Secao", parent=styles["Heading2"], fontSize=13, leading=16, spaceBefore=12, spaceAfter=6))
styles.add(ParagraphStyle(name="Texto", parent=styles["BodyText"], fontSize=10, leading=14, spaceAfter=7))
styles.add(ParagraphStyle(name="Legenda", parent=styles["BodyText"], fontSize=9, leading=12, leftIndent=8, spaceAfter=6))

story = [
    Paragraph("Relatório sucinto: Chat via UDP", styles["TituloAtividade"]),
    Paragraph("Atividade prática de Redes de Computadores", styles["Texto"]),
    Paragraph("1. Estratégia adotada", styles["Secao"]),
    Paragraph("A aplicação foi dividida em um remetente (chat_sender.py) e um destinatário (chat_receiver.py). Os dois componentes usam sockets UDP (SOCK_DGRAM) e trocam mensagens de texto com campos separados pelo caractere |.", styles["Texto"]),
    Paragraph("Cada mensagem recebe um identificador inteiro sequencial e é enviada no formato MSG|&lt;ID&gt;|&lt;CONTEUDO&gt;. Antes do envio, o remetente registra o par ID/texto em pending_messages. Assim, a mensagem começa no estado Pendente (Check Cinza).", styles["Texto"]),
    Paragraph("O destinatário escuta a porta UDP 5001 e aplica DROP_RATE = 0.4 para simular perdas. Quando processa um pacote, imprime a mensagem e responde com DELIVERED|&lt;ID&gt;. Uma thread separada no remetente escuta os recibos, remove a entrada confirmada e exibe Entregue (Check Azul). O dicionário é protegido por threading.Lock.", styles["Texto"]),
    Paragraph("2. Captura de tela 1: perda proposital", styles["Secao"]),
    Paragraph("O primeiro cenário deve mostrar o remetente com uma mensagem pendente, o receptor indicando o descarte artificial e o comando /status exibindo a pendência.", styles["Texto"]),
    Preformatted("Remetente: [Pendente] ID 1: mensagem de teste\nReceptor:  [CANAL] Pacote descartado artificialmente!\n/status -> Mensagens pendentes: 1", styles["Code"]),
    Paragraph("Print realizado no terminal:", styles["Legenda"]),
    Preformatted("==========================================================\n RECEPTOR UDP - EVIDENCIA DA ATIVIDADE\n Porta: 5001 | Perda simulada: 40.0%\n Aguardando mensagens...\n==========================================================\n\n[DESCARTE] Pacote descartado artificialmente!", styles["Code"]),
    Paragraph("No remetente, /status mostrou Mensagens pendentes: 1 e a mensagem ID 1 em estado PENDENTE - CHECK CINZA.", styles["Texto"]),
    Paragraph("3. Captura de tela 2: reenvio e confirmação", styles["Secao"]),
    Paragraph("Com a mensagem pendente, /reenviar retransmite os registros. Quando o receptor processa o pacote, ele responde com o recibo e o remetente remove a mensagem.", styles["Texto"]),
    Preformatted("Remetente: [Reenviado] ID 1: mensagem de teste\nReceptor:  [MSG 1] mensagem de teste\nRemetente: [✓✓ Entregue] ID 1: mensagem de teste\n/status -> Mensagens pendentes: 0", styles["Code"]),
    Paragraph("As capturas reais dos dois momentos devem acompanhar este relatório na entrega do repositório.", styles["Legenda"]),
    Paragraph("Print realizado no terminal:", styles["Legenda"]),
    Preformatted("[RECEBIDA] ID 1: mensagem de teste UDP\n[ACK ENVIADO] DELIVERED|1\n[REENVIADO] ID 1: mensagem de teste UDP", styles["Code"]),
    Paragraph("O teste também confirmou o protocolo com DELIVERED|42 recebido pelo remetente. As imagens dos dois terminais devem ser anexadas ao PDF quando disponíveis.", styles["Texto"]),
    Paragraph("4. Aplicação x TCP", styles["Secao"]),
    Paragraph("Neste exercício, a confiabilidade é construída na camada de aplicação. O programa atribui IDs, mantém pendências, gera recibos e retransmite mensagens sem confirmação. Isso permite controlar o significado de entregue, mas exige código adicional.", styles["Texto"]),
    Paragraph("No TCP, a camada de transporte oferece conexão, ordenação, retransmissão e confirmação de recebimento dos segmentos. A aplicação recebe um fluxo confiável de bytes. Porém, uma confirmação TCP indica chegada ao outro endpoint TCP; não garante que a aplicação destinatária exibiu ou processou a mensagem. O recibo DELIVERED|&lt;ID&gt; é uma confirmação semântica da aplicação.", styles["Texto"]),
    Paragraph("5. Conformidade", styles["Secao"]),
    Paragraph("Comunicação exclusivamente UDP/SOCK_DGRAM; porta 5001; perda simulada de 40%; formatos MSG e DELIVERED; IDs sequenciais; thread de recibos; comandos /status e /reenviar.", styles["Texto"]),
]

doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=2 * cm, leftMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=1.8 * cm)
doc.build(story)
print(OUTPUT)
