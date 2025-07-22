from datetime import datetime
import time
from utils.utilsSQL import insertJogo, insertNoticia, jogoNoDB
from utils.utilsAPI import nomeJogo, noticiasJogo

def verificaNomeJogo(jogoDict, appid):
    '''Obtem nome do jogo ou retorna `Erro`'''
    try:
        return jogoDict[str(appid)]["data"]["name"]
    except:
        return "Erro"

def converterTimestamp(timestamp):
    '''Converte o valor de tempo de string para Data Hora'''
    try:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"[data] Erro ao converter timestamp: {type(e).__name__} - {e}")
        return "1970-01-01 00:00:00"

def processarNoticia(appid, noticia, username, categoria):
    '''Separa as informações das noticias em suas variaveis'''
    gid = noticia.get("gid", "Sem gid")
    title = noticia.get("title", "Sem title")
    url = noticia.get("url", "Sem url")
    content = noticia.get("contents", "Sem contents")
    data = converterTimestamp(noticia.get("date", time.time()))
    try:
        insertNoticia(appid, gid, title, url, content, data)
    except Exception as e:
        print(f"[{categoria}][insertNoticia] Erro ao inserir notícia (gid={gid}, appid={appid}, user='{username}'): {type(e).__name__} - {e}")

def processarJogo(appid, username, categoria):
    '''Responsavel por controlar e processar as informações'''
    try:
        try:
            nome = jogoNoDB(appid)
            if not nome:
                nomeAPI = nomeJogo(appid)
                nome = verificaNomeJogo(nomeAPI, appid)
        except Exception as e:
            print(f"Erro ao verificar no banco ou converter nome {e}")
        news = noticiasJogo(appid)

        try:
            insertJogo(appid, username, categoria, nome)
        except Exception as e:
            print(f"[{categoria}][insertJogo] Erro ao inserir jogo '{nome}' (appid={appid}) para usuário '{username}': {type(e).__name__} - {e}")

        for noticia in news["appnews"]["newsitems"]:
            processarNoticia(appid, noticia, username, categoria)

        print(f"Jogo {appid} adicionado para {username} em {categoria}")
    except Exception as e:
        print(f"[{categoria}][Geral] Erro inesperado ao processar appid={appid} para user='{username}': {type(e).__name__} - {e}")