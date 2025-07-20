import requests, time

def jogosWishlist(key, userId, tentativas=5):
    '''Busca o `ID` de todos os jogos da `Lista de desejos` na API da steam, tenta ao menos 5 vezes com um intervalo de 10 segundos'''
    try:
        wishlistResponse = requests.get(f"https://api.steampowered.com/IWishlistService/GetWishlist/v1/?key={key}&steamid={userId}")
        wishlistResponse.raise_for_status()
        return wishlistResponse.json()
    except Exception as e:
        if tentativas > 0:
            print(f"Erro ao buscar user {userId}, para wishlist, tentando novamente em 60s... ({tentativas} tentativas restantes)")
            time.sleep(60)
            return nomeJogo(key, userId, tentativas - 1)
        else:
            print(f"Falha permanente ao buscar appid {userId}: {e}")
            return {f"{userId}": {"data": {"name": "Erro"}}}

def jogosBiblioteca(key, userId, tentativas=5):
    '''Busca o `ID` de todos os jogos da `Biblioteca` na API da steam, tenta ao menos 5 vezes com um intervalo de 10 segundos'''
    try:
        bibliotecaResponse = requests.get(f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={userId}&format=json")
        bibliotecaResponse.raise_for_status()
        return bibliotecaResponse.json()
    except Exception as e:
        if tentativas > 0:
            print(f"Erro ao buscar user {userId}, para bilioteca,tentando novamente em 60s... ({tentativas} tentativas restantes)")
            time.sleep(60)
            return nomeJogo(key, userId, tentativas - 1)
        else:
            print(f"Falha permanente ao buscar appid {userId}: {e}")
            return {f"{userId}": {"data": {"name": "Erro"}}}

def nomeJogo(appId, tentativas = 5):
    '''Busca o `Nome` do jogo com base no `appID` na API da steam, tenta ao menos 5 vezes com um intervalo de 10 segundos'''
    try:
        jogosResponse = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appId}")
        jogosResponse.raise_for_status()
        return jogosResponse.json()
    except Exception as e:
        if tentativas > 0:
            print(f"Erro ao buscar appid {appId}, para nome do jogo, tentando novamente em 60s... ({tentativas} tentativas restantes)")
            time.sleep(60)
            return nomeJogo(appId, tentativas - 1)
        else:
            print(f"Falha permanente ao buscar appid {appId}: {e}")
            return {f"{appId}": {"data": {"name": "Erro"}}}

def noticiasJogo(appId, tentativas=5):
    '''Verifica as 10 noticias mais recentes na API da Steam, tenta ao menos 5 vezes com um intervalo de 10 segundos'''
    try:
        newsResponse = requests.get(f"https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={appId}&count=10&maxlength=300&format=json")
        newsResponse.raise_for_status()
        return newsResponse.json()
    except Exception as e:
        if tentativas > 0:
            print(f"Erro ao buscar appid {appId}, para noticias do jogo, tentando novamente em 60s... ({tentativas} tentativas restantes)")
            time.sleep(60)
            return nomeJogo(appId, tentativas - 1)
        else:
            print(f"Falha permanente ao buscar appid {appId}: {e}")
            return {f"{appId}": {"data": {"name": "Erro"}}}