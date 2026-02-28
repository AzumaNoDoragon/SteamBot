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


def valorAtualSteam(appId, tentativas=5):
    try:
        urlRequest = f"https://store.steampowered.com/api/appdetails?appids={appId}&cc=br&filters=price_overview"
        valorAtual = requisitaAPI(urlRequest)
        
        if valorAtual is None:
            raise ValueError("Resposta da API inválida ou nula para newsResponse.")
        
        return valorAtual.json()
    except Exception as e:
        if tentativas > 0:
            tempoEntreRequisicao(urlRequest, tentativas)
            return valorAtualSteam(appId, tentativas - 1)
        else:
            print(f"Falha permanente no valorAtualSteam ao buscar appid {appId}: {e}")
            return {f"{appId}": {"data": {"name": "Erro"}}}

def menorPreçoITDA(appid, ITRD_KEY):
    try:
        lookup_url = "https://api.isthereanydeal.com/games/lookup/v1"
        r = requests.get(lookup_url, params={"key": ITRD_KEY, "appid": appid})
        r.raise_for_status()
        data = r.json()

        gameId = data.get("game", {}).get("id")
        if not gameId:
            return None

        lowPrice = f"https://api.isthereanydeal.com/games/storelow/v2?key={ITRD_KEY}&country=BR&shops=61"
        response = requests.post(lowPrice, json=[gameId])
        response.raise_for_status()
        low = response.json()
        if low and len(low) > 0:
            lows = low[0].get("lows", [])
            if lows:
                return lows[0]["price"]["amount"]
    except Exception as e:
        print(f"Erro ITAD (AppID {appid}): {e}")
        return None

def valorRegular(appid):
    valor = valorAtualSteam(appid)
    steam_data = valor.get(str(appid))
    
    if not steam_data:
        print("Resposta inválida da Steam")
        return

    if steam_data.get("success") is False:
        print("Jogo inválido ou removido da Steam")
        return

    data_field = steam_data.get("data")

    if not data_field or not isinstance(data_field, dict):
        print("Jogo sem dados válidos (removido ou indisponível)")
        return

    priceInfo = data_field.get("price_overview")

    if not priceInfo:
        print("Jogo sem preço (gratuito ou sem overview)")
        return
    
    return priceInfo["final"] / 100