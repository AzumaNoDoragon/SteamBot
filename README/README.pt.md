# SteamBot - Notícias Automáticas da Steam por E-mail

SteamBot é um projeto em Python que coleta automaticamente notícias dos jogos da sua biblioteca e wishlist da Steam, organiza as informações e envia um resumo em formato HTML por e-mail. É a solução ideal para quem deseja acompanhar atualizações e novidades dos seus jogos favoritos sem precisar acessar a Steam manualmente.
A Steam mantém um histórico de notícias apenas para jogos jogados nos últimos seis meses, o que pode fazer com que você perca informações importantes sobre títulos antigos. O SteamBot resolve esse problema, garantindo que nenhuma novidade passe despercebida, mesmo para jogos que você não acessa há muito tempo.

## Funcionalidades

- Busca automática dos jogos da biblioteca e wishlist de múltiplos usuários via API da Steam.
- Consulta das notícias mais recentes de cada jogo.
- Armazenamento das notícias e jogos em banco SQLite, evitando duplicidade.
- Geração de e-mail HTML personalizado para cada usuário, agrupando notícias por biblioteca e wishlist.
- Envio automático de e-mails via Gmail.
- Validação de imagens dos jogos para exibição nos cards.
- Limpeza automática das notícias antigas, mantendo apenas as 10 mais recentes por jogo.
- Correção automática de nomes de jogos que não foram buscados corretamente.

## Requisitos

- Python 3.7 ou superior
- Pacotes: `requests`, `smtplib`, `email`
- Banco de dados SQLite (criado automaticamente)
- Conta Gmail para envio dos e-mails (recomenda-se senha de app)
- Chave de API da Steam
- Arquivo de configuração `utils/secrets.json` com dados dos usuários e e-mail

## Como executar

1. Clone ou baixe o repositório.
2. Instale as dependências Python:
   ```bash
   pip install requests
   ```
3. Configure o arquivo `utils/secrets.json` com sua chave da Steam, e-mails dos usuários e credenciais do Gmail.
4. Execute o script principal:
   ```bash
   python SteamBot.py
   ```
5. O programa irá buscar os jogos, coletar notícias, gerar o HTML e enviar o e-mail para os destinatários configurados.
6. O HTML gerado também ficará salvo em `utils/card.html`.

> **Notas**
> - O envio de e-mail utiliza SMTP do Gmail. Certifique-se de liberar acesso ou usar senha de app.
> - O banco de dados é criado automaticamente e armazena apenas as últimas 10 notícias de cada jogo.
> - O sistema evita envio duplicado de notícias e corrige nomes de jogos com erro de busca.

## Estrutura dos arquivos

- `SteamBot.py`: Script principal, orquestra toda a lógica de busca, armazenamento e envio.
- `utils/utilsAPI.py`: Funções para acessar as APIs da Steam.
- `utils/utilsSQL.py`: Funções para manipulação do banco SQLite.
- `utils/utilsEmail.py`: Funções para montagem do HTML e envio de e-mail.
- `utils/secrets.json`: Configuração dos usuários e credenciais (não incluído no repositório).
- `utils/card.html`: Arquivo gerado com o conteúdo do e-mail em HTML.

## Exemplo de uso

Ao executar o script, cada usuário cadastrado receberá um e-mail semelhante a este:

![Exemplo de Card HTML]()

## Licença

Este projeto é distribuído para fins educacionais e pessoais. Consulte a Steam para uso comercial de suas APIs.

---

Desenvolvido com dedicação e Python, por [AzumaNoDoragon](https://steamcommunity.com/id/AzumaNoDoragon/) um desenvolvedor e gamer.