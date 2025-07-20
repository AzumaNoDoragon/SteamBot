import requests
import smtplib
from email.message import EmailMessage

def enviaEmailGmail(emailBot, senha, emailDestino, emailHtml):
    '''Monta o email, com remetente, destinatario, assunto e outros.'''
    remetente = f"{emailBot}"
    senha_app = f"{senha}"

    msg = EmailMessage()
    msg['Subject'] = "Steam News"
    msg['From'] = remetente
    msg['To'] = emailDestino
    msg.set_content('Seu cliente de e-mail não suporta HTML.')
    msg.add_alternative(emailHtml, subtype='html')

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(remetente, senha_app)
            smtp.send_message(msg)
        print(f"Email enviado para {emailDestino}")
        return True
    except Exception as e:
        print(f"Erro ao enviar para {emailDestino}: {e}")
        return False
    
def imagem_valida(appId):
    '''Seleciona qual a imagem está funcionado para determinado jogo, visto que nem todos os jogos possuem todos tipos'''
    urls = [
        f"https://cdn.akamai.steamstatic.com/steam/apps/{appId}/hero_capsule.jpg",
        f"https://cdn.akamai.steamstatic.com/steam/apps/{appId}/library_600x900.jpg",
        f"https://cdn.akamai.steamstatic.com/steam/apps/{appId}/header.jpg",
        f"https://cdn.akamai.steamstatic.com/steam/apps/{appId}/capsule_467x181.jpg",
        f"https://cdn.akamai.steamstatic.com/steam/apps/{appId}/capsule_231x87.jpg",
        f"https://cdn.akamai.steamstatic.com/steam/apps/{appId}/logo.png",
        f"https://cdn.akamai.steamstatic.com/steam/apps/{appId}/page_bg_raw.jpg",
        f"https://cdn.akamai.steamstatic.com/steam/apps/{appId}/background.jpg"
    ]
    
    bug_image = "https://img.freepik.com/vetores-gratis/glitch-error-404-page-background_23-2148072533.jpg"
    
    for url in urls:
        try:
            resposta = requests.head(url, timeout=3)
            if resposta.status_code == 200:
                return url
        except requests.RequestException:
            continue
    return bug_image

def corpoEmail(nome, title, data, content, url, appId):
    '''Monta o corpo de email, se replicando para quantas noticias tem'''
    imagem = imagem_valida(appId)
    return f"""
        <div style="background-color: #fefefe; border-radius: 8px; padding: 10px; display: flex; justify-content: space-between; margin-bottom: 10px;">
            <div style="width: 120px; min-width: 100px; align-self: Right;">
                <a href="{url}" target="_blank">
                    <img src="{imagem}" alt="Imagem do jogo" style="width: 100%; border-radius: 6px;">
                </a>
            </div>
            <div style="flex: 1; padding-left: 10px;">
                <h4 style="margin: 5px 0; word-break: break-word;">{nome}</h4>
                <p style="margin: 5px 0; word-break: break-word;"><strong>Título:</strong> {title}</p>
                <p style="margin: 5px 0; word-break: break-word;"><strong>Data:</strong> {data}</p>
                <p style="margin: 5px 0; word-break: break-word;"><strong>Descrição:</strong> {content}</p>
            </div>
        </div>
    """

def htmlInicio():
    '''Inicio padrão para o corpo do email'''
    return """
        <!DOCTYPE html>
        <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <title>Notícias da Steam</title>
            </head>
            <body style="background-color: #f5f5f5; padding: 20px; font-family: Arial, sans-serif;">
                <h1 style="text-align: center; color: #333;">Notícias</h1>
    """

def htmlFinal():
    '''Final padrão para o corpo do email'''
    return """
            </body>
        </html>
    """