import sqlite3 as sql

def conectar():
    '''Faz a conexão com o banco `dados.db` e ativa a chave estrangeira'''
    conn = sql.connect("dados.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def criaTabelas():
    '''Cria as tabelas `jogos` e `noticias`, com seus atributos determinantes, caso não existam.'''
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jogos(
            appid TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            categoria TEXT NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS noticias(
            appid TEXT NOT NULL,
            gid TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            content TEXT NOT NULL,
            data DATE NOT NULL,
            enviado INTEGER NOT NULL,
            PRIMARY KEY (appid, gid),                   
            FOREIGN KEY (appid) REFERENCES jogos(appid)
        )
    ''')
    conn.commit()
    conn.close()

def insertJogo(appId, username, categoria, nome):
    '''Insere o jogo, caso não exista.'''
    conn = conectar()
    query = f"INSERT OR IGNORE INTO jogos (appid, username, categoria, name) VALUES (?, ?, ?, ?)"
    conn.execute(query, (appId, username, categoria, nome))
    conn.commit()
    conn.close()
    
def insertNoticia(appId, gid, title, url, content, data, enviado):
    '''Insere as noticias mais recentes, caso exista novas noticias.'''
    conn = conectar()
    query = f"INSERT OR IGNORE INTO noticias (appid, gid, title, url, content, data, enviado) VALUES (?, ?, ?, ?, ?, ?, ?)"
    conn.execute(query, (appId, gid, title, url, content, data, enviado))
    conn.commit()
    conn.close()

def selectNovasNoticias():
    '''Seleciona as noticias com `enviado = 0` para criar os card de noticia para enviar pelo e-mail'''
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            noticias.*, jogos.name, jogos.username, jogos.categoria
        FROM
            noticias
        INNER JOIN
            jogos On noticias.appid = jogos.appid
        WHERE
            noticias.enviado = 0
        ORDER BY
            jogos.username,
            jogos.categoria = 'wishlist',
            noticias.data DESC
    ''')
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def buscaNomesErros():
    '''Pega os nomes com `Erro` do banco de dados'''
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            appid
        FROM 
            jogos
        WHERE 
            name = "Erro"
    ''')
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def arrumaNomes(nome, appid):
    '''Tenta corrigir os nomes dos bancos de dados com `Erro`'''
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE 
            jogos 
        SET 
            name = ?
        WHERE 
            appid = ?
    ''', (nome, appid))
    conn.commit()
    conn.close()

def manterUltimas10Noticias(appid):
    '''Deleta do banco todas as noticias excedidas de jogos em mais de 10'''
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            DELETE FROM noticias
            WHERE rowid IN (
                SELECT rowid FROM noticias
                WHERE appid = ?
                ORDER BY data DESC
                LIMIT -1 OFFSET 10
            )
        ''', (appid,))
        conn.commit()
        print(f"Noticias antigas removidas para appid {appid}")
    except Exception as e:
        print(f"Erro ao limpar noticias para {appid}: {e}")
        conn.rollback()
    finally:
        conn.close()

def limparNoticiasAntigas():
    '''Seleciona os appId para selecionar o que pode ser apagado de noticias'''
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT appid FROM noticias')
    appids = [row[0] for row in cursor.fetchall()]
    conn.close()

    for appid in appids:
        manterUltimas10Noticias(appid)
