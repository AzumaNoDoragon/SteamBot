print("Importanto bibliotecas...")
import json
from utils.utilsSQL import criaTabelas, conectar, selectNovasNoticias, buscaNomesErros, arrumaNomes, limparNoticiasAntigas
from utils.utilsAPI import jogosWishlist, jogosBiblioteca, nomeJogo
from utils.utilsEmail import corpoEmail, htmlInicio, htmlFinal, enviaEmailGmail
from utils.utilsSteam import processarJogo
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo
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

    for item in jogosWishlist(key, userId)["response"]["items"]:
        processarJogo(item["appid"], username, "wishlist")

    for item in jogosBiblioteca(key, userId)["response"]["games"]:
        processarJogo(item["appid"], username, "biblioteca")

# jogo padrão Steam
processarJogo(593110, "Steam", "steam")

conn = conectar()
cursor = conn.cursor()
email = []

try:
    noticiasPorUsuario = defaultdict(lambda: {"steam": [], "biblioteca": [], "wishlist": []})
    novasNoticias = selectNovasNoticias("Steam")
    for noticia in novasNoticias:
        appid, gid, titulo, url, conteudo, data, enviado, nome, username, categoria = noticia
        noticiasPorUsuario[username][categoria].append(
            (appid, gid, titulo, url, conteudo, data, nome)
        )
    for user in accounts:
        userNews = user.get("username")
        novasNoticias = selectNovasNoticias(userNews)
        for noticia in novasNoticias:
            appid, gid, titulo, url, conteudo, data, enviado, nome, username, categoria = noticia
            noticiasPorUsuario[username][categoria].append(
                (appid, gid, titulo, url, conteudo, data, nome)
            )

    for usuario, origens in noticiasPorUsuario.items():
        email.append(f"""
            <div style="background-color: #738496; margin-bottom: 30px; padding: 20px; border-radius: 12px;">
                <h2 style="font-family:Arial; color: white; margin-top: 0;">Notícias de {usuario}</h2>
        """)

        for tipo in ["steam", "biblioteca", "wishlist"]:
            noticias = origens.get(tipo, [])
            if noticias:
                if tipo == "biblioteca":
                    categoria = "Biblioteca"
                elif tipo == "wishlist":
                    categoria = "Wishlist"
                else:
                    categoria = "Steam"

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
        agora = datetime.now(ZoneInfo("America/Sao_Paulo"))
        emailFinal = htmlInicio(agora) + "\n".join(email) + htmlFinal()
        with open("index.html", "w", encoding="utf-8") as arquivo:
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