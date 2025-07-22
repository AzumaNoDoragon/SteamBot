import requests, time

def requisitaAPI(urlRequest):
    '''Centraliza a lógica de requisição, com timeout de 5s para conexão e 10 para resposta'''
    try:
        response = requests.get(urlRequest, timeout=(5, 10))
        if response.status_code == 200:
            return response
        else:
            print(f"Resposta recebida com status {response.status_code} para {urlRequest}")
            return None

    except requests.exceptions.Timeout:
        print("A requisição demorou demais e foi cancelada.")
    except requests.RequestException as e:
        print("Erro geral de rede:", e)
    
    return None

def tempoEntreRequisicao(urlRequest, tentativas):
    '''Retorna a informação de erro e espera 60s para outra requisição'''
    print(f"Erro ao buscar {urlRequest}, tentando novamente em 60s... ({tentativas} tentativas restantes)")
    time.sleep(60)

def jogosWishlist(key, userId, tentativas=5):
    '''Busca o `ID` de todos os jogos da `Lista de desejos` na API da steam, tenta ao menos 5 vezes com um intervalo de 10 segundos'''
    try:
        urlRequest = f"https://api.steampowered.com/IWishlistService/GetWishlist/v1/?key={key}&steamid={userId}"
        wishlistResponse = requisitaAPI(urlRequest)
        
        if wishlistResponse is None:
            raise ValueError("Resposta da API inválida ou nula para wishlistResponse.")

        return wishlistResponse.json()
    except Exception as e:
        if tentativas > 0:
            tempoEntreRequisicao(urlRequest, tentativas)
            return jogosWishlist(key, userId, tentativas - 1)
        else:
            print(f"Falha permanente no jogosWishlist ao buscar appid {userId}: {e}")
            return {f"{userId}": {"data": {"name": "Erro"}}}

def jogosBiblioteca(key, userId, tentativas=5):
    '''Busca o `ID` de todos os jogos da `Biblioteca` na API da steam, tenta ao menos 5 vezes com um intervalo de 10 segundos'''
    try:
        urlRequest = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={userId}&format=json"
        bibliotecaResponse = requisitaAPI(urlRequest)

        if bibliotecaResponse is None:
            raise ValueError("Resposta da API inválida ou nula para bibliotecaResponse.")

        return bibliotecaResponse.json()
    except Exception as e:
        if tentativas > 0:
            tempoEntreRequisicao(urlRequest, tentativas)
            return jogosBiblioteca(key, userId, tentativas - 1)
        else:
            print(f"Falha permanente no jogosBiblioteca ao buscar appid {userId}: {e}")
            return {f"{userId}": {"data": {"name": "Erro"}}}

def nomeJogo(appId, tentativas = 5):
    '''Busca o `Nome` do jogo com base no `appID` na API da steam, tenta ao menos 5 vezes com um intervalo de 10 segundos'''
    try:
        urlRequest = f"https://store.steampowered.com/api/appdetails?appids={appId}"
        jogosResponse = requisitaAPI(urlRequest)

        if jogosResponse is None:
            raise ValueError("Resposta da API inválida ou nula para jogosResponse.")

        return jogosResponse.json()
    except Exception as e:
        if tentativas > 0:
            tempoEntreRequisicao(urlRequest, tentativas)
            return nomeJogo(appId, tentativas - 1)
        else:
            print(f"Falha permanente no nomeJogo ao buscar appid {appId}: {e}")
            return {f"{appId}": {"data": {"name": "Erro"}}}

def noticiasJogo(appId, tentativas=5):
    '''Verifica as 10 noticias mais recentes na API da Steam, tenta ao menos 5 vezes com um intervalo de 10 segundos'''
    try:
        urlRequest = f"https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={appId}&count=10&maxlength=300&format=json"
        newsResponse = requisitaAPI(urlRequest)

        if newsResponse is None:
            raise ValueError("Resposta da API inválida ou nula para newsResponse.")
        
        return newsResponse.json()
    except Exception as e:
        if tentativas > 0:
            tempoEntreRequisicao(urlRequest, tentativas)
            return noticiasJogo(appId, tentativas - 1)
        else:
            print(f"Falha permanente no noticiasJogo ao buscar appid {appId}: {e}")
            return {f"{appId}": {"data": {"name": "Erro"}}}
