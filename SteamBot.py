print("Importanto bibliotecas...")
import json
from utils.utilsSQL import *
from utils.utilsAPI import *
from utils.utilsEmail import *
from collections import defaultdict
from datetime import datetime
print("Iniciando...")
criaTabelas()
with open("utils/secrets.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)
    emailconf = dados["response"]["email"][0]
    emailBot = emailconf["email"]
    senha = emailconf["senha"]
    key = emailconf["key"]
    emailDestino = []
    for user in dados["response"]["accounts"]:
        email = user.get("email")
        if email != "null":
            emailDestino.append(email)

accounts = dados["response"]["accounts"]
for user in accounts:
    username = user["username"]
    userId = user["userid"]

    wishlist = jogosWishlist(key, userId)
    for item in wishlist["response"]["items"]:
        appId = item["appid"]

        try:
            jogo = nomeJogo(appId)
            news = noticiasJogo(appId)
            try:
                nome = jogo[f"{appId}"]["data"]["name"]
            except:
                nome = "Erro"
            
            try:
                insertJogo(appId, username, "wishlist", nome)
            except Exception as e:
                print(f"[wishlist][insertJogo] Erro ao inserir jogo '{nome}' (appid={appId}) para usuário '{username}': {type(e).__name__} - {e}")

            for noticia in news["appnews"]["newsitems"]:
                enviado = 1
                gid = noticia.get("gid", "Sem gid")
                title = noticia.get("title" , "Sem title")
                url = noticia.get("url" , "Sem url") 
                content = noticia.get("contents" , "Sem contents")
                try:
                    timestamp = noticia.get("date", time.time())
                    data = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    data = "1970-01-01 00:00:00"
                    print(f"[wishlist][dataNoticia] Erro ao converter data da notícia (gid={gid}, appid={appId}): {type(e).__name__} - {e}")

                try:
                    insertNoticia(appId, gid, title, url, content, data, enviado)
                except Exception as e:
                    print(f"[wishlist][insertNoticia] Erro ao inserir notícia (gid={gid}, appid={appId}, user='{username}'): {type(e).__name__} - {e}")
            print(f"Jogo {appId} adicionado para {username} na wishlist")
        except Exception as e:
            print(f"[wishlist][Geral] Erro inesperado ao processar appid={appId} para user='{username}': {type(e).__name__} - {e}")
    
    biblioteca = jogosBiblioteca(key, userId)
    for item in biblioteca["response"]["games"]:
        appId = item["appid"]

        try:
            jogo = nomeJogo(appId)
            news = noticiasJogo(appId)
            try:
                nome = jogo[f"{appId}"]["data"]["name"]
            except:
                nome = "Erro"
            
            try:
                insertJogo(appId, username, "biblioteca", nome)
            except Exception as e:
                print(f"[biblioteca][insertJogo] Erro ao inserir jogo '{nome}' (appid={appId}) para usuário '{username}': {type(e).__name__} - {e}")

            for noticia in news["appnews"]["newsitems"]:
                enviado = 0
                gid = noticia.get("gid", "Sem gid")
                title = noticia.get("title" , "Sem title")
                url = noticia.get("url" , "Sem url") 
                content = noticia.get("contents" , "Sem contents")
                try:
                    timestamp = noticia.get("date", time.time())
                    data = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    data = "1970-01-01 00:00:00"
                    print(f"[biblioteca][dataNoticia] Erro ao converter data da notícia (gid={gid}, appid={appId}): {type(e).__name__} - {e}")

                try:
                    insertNoticia(appId, gid, title, url, content, data, enviado)
                except Exception as e:
                    print(f"[biblioteca][insertNoticia] Erro ao inserir notícia (gid={gid}, appid={appId}, user='{username}'): {type(e).__name__} - {e}")
                print(f"Jogo {appId} adicionado para {username} na biblioteca")
        except Exception as e:
            print(f"[biblioteca][Geral] Erro inesperado ao processar appid={appId} para user='{username}': {type(e).__name__} - {e}")

try:
    appIdSteam = 593110
    steamUser = "Steam"
    jogo = nomeJogo(appIdSteam)
    news = noticiasJogo(appIdSteam)
    try:
        nome = jogo[f"{appIdSteam}"]["data"]["name"]
    except:
        nome = "Erro"
    
    try:
        insertJogo(appIdSteam, steamUser, "steam", nome)
    except Exception as e:
        print(f"[steam][insertJogo] Erro ao inserir jogo '{nome}' (appid={appIdSteam}) para usuário '{steamUser}': {type(e).__name__} - {e}")
    
    for noticia in news["appnews"]["newsitems"]:
        enviado = 0
        gid = noticia.get("gid", "Sem gid")
        title = noticia.get("title" , "Sem title")
        url = noticia.get("url" , "Sem url") 
        content = noticia.get("contents" , "Sem contents")
        try:
            timestamp = noticia.get("date", time.time())
            data = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            data = "1970-01-01 00:00:00"
            print(f"[steam][dataNoticia] Erro ao converter data da notícia (gid={gid}, appid={appIdSteam}): {type(e).__name__} - {e}")

        try:
            insertNoticia(appIdSteam, gid, title, url, content, data, enviado)
        except Exception as e:
            print(f"[steam][insertNoticia] Erro ao inserir notícia (gid={gid}, appid={appIdSteam}, user='{steamUser}'): {type(e).__name__} - {e}")
    print(f"Jogo {appIdSteam} adicionado para {steamUser} na steam")
except Exception as e:
    print(f"[steam][Geral] Erro inesperado ao processar appid={appIdSteam} para user='{steamUser}': {type(e).__name__} - {e}")

conn = conectar()
cursor = conn.cursor()
email = []
novasNoticias = selectNovasNoticias()

try:
    noticiasSteam = defaultdict(lambda: {"steam": []})

    for noticia in novasNoticias:
        appid, gid, titulo, url, conteudo, data, enviado, nome, username, categoria = noticia
        noticiasSteam[username][categoria].append(
            (appid, gid, titulo, url, conteudo, data, nome)
        )

    for usuario, origens in noticiasSteam.items():
        email.append(f"""
            <div style="background-color: #738496; margin-bottom: 30px; padding: 20px; border-radius: 12px;">
                <h2 style="font-family:Arial; color: white; margin-top: 0;">Notícias da Steam</h2>
        """)

        for tipo in ["steam"]:
            noticias = origens.get(tipo, [])
            if noticias:
                categoria = "steam"
                email.append(f"""
                    <div style="background-color: #90a0b0; padding: 15px; border-radius: 8px; margin-top: 15px;">
                        <h3 style="font-family:Arial; color:#ffffff; margin-top: 0;">{categoria}</h3>
                """)

                for noticia in noticias:
                    appid, gid, titulo, url, conteudo, data, nomeDoJogo = noticia
                    cursor.execute('''
                        UPDATE noticias
                        SET enviado = 1
                        WHERE appid = ? AND gid = ?
                    ''', (appid, gid))
                    email.append(corpoEmail(nomeDoJogo, titulo, data, conteudo, url, appid))
                
                email.append("</div>")
        email.append("</div>")
except Exception as e:
    print(f"Erro ao criar e atualizar as noticias da Steam {e}")

try:
    noticiasPorUsuario = defaultdict(lambda: {"biblioteca": [], "wishlist": []})

    for noticia in novasNoticias:
        appid, gid, titulo, url, conteudo, data, enviado, nome, username, categoria = noticia
        noticiasPorUsuario[username][categoria].append(
            (appid, gid, titulo, url, conteudo, data, nome)
        )

    for usuario, origens in noticiasPorUsuario.items():
        email.append(f"""
            <div style="background-color: #738496; margin-bottom: 30px; padding: 20px; border-radius: 12px;">
                <h2 style="font-family:Arial; color: white; margin-top: 0;">Notícias dos jogos de {usuario}</h2>
        """)

        for tipo in ["biblioteca", "wishlist"]:
            noticias = origens.get(tipo, [])
            if noticias:
                categoria = "Biblioteca" if tipo == "biblioteca" else "Wishlist"
                email.append(f"""
                    <div style="background-color: #90a0b0; padding: 15px; border-radius: 8px; margin-top: 15px;">
                        <h3 style="font-family:Arial; color:#ffffff; margin-top: 0;">{categoria}</h3>
                """)

                for noticia in noticias:
                    appid, gid, titulo, url, conteudo, data, nomeDoJogo = noticia
                    cursor.execute('''
                        UPDATE noticias
                        SET enviado = 1
                        WHERE appid = ? AND gid = ?
                    ''', (appid, gid))
                    email.append(corpoEmail(nomeDoJogo, titulo, data, conteudo, url, appid))
                
                email.append("</div>")
        email.append("</div>")
except Exception as e:
    print(f"Erro ao criar e atualizar as noticias de user {e}")

try:
    if email:
        agora = datetime.now()
        emailFinal = htmlInicio(agora) + "\n".join(email) + htmlFinal()
        with open("utils/index.html", "w", encoding="utf-8") as arquivo:
            arquivo.write(emailFinal)

        try:
            emailEnviado = enviaEmailGmail(emailBot, senha, emailDestino, emailFinal)
            if emailEnviado:
                conn.commit()
            else:
                conn.rollback()
        except Exception as e:
            conn.rollback()
            print(f"Erro ao inserir novas noticias ao banco de dados: {e}")
        finally:
            conn.close()
except Exception as e:
    print(f"Erro ao criar o email {e}")

nomesErrados = buscaNomesErros()
for (appId,) in nomesErrados:
    nomeCerto = nomeJogo(appId)
    try:
        nomeCerto = nomeCerto[f"{appId}"]["data"]["name"]
    except:
        nomeCerto = "Nameless"
    arrumaNomes(nomeCerto, appId)

limparNoticiasAntigas()
print("Fim da execução...")