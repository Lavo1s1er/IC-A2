import yahooquery as yq


def obtem_cotacao(acao, dias):
    """
    Obtém a cotação dos últimos N dias da ação

    Recebe o código da ação e o número de dias, busca as cotações utilizando a
    biblioteca yahooquery e retorna um DataFrame contendo as informações obtidas.

    :param acao: Código da ação
    :type acao: str
    :param dias: Quantos dias de cotações devem ser retornados
    :type dias: int
    :return: As cotações dos últimos N dias
    :rtype: pandas.core.frame.DataFrame
    """
    ticker = yq.Ticker(acao)
    texto_historico = f"{dias}d"

    cotacao = ticker.history(texto_historico)
    return cotacao


def moeda_em_real(moeda):
    """
    Obtém o valor de uma moeda em reais.

    Recebe o código de uma moeda, busca o seu valor em reais utilizando a
    biblioteca yahooquery e retorna esse valor.

    :param moeda: O código da moeda
    :type moeda: str
    :return: O valor da moeda em reais
    :rtype: float
    """
    texto_conversao = f"{moeda}BRL=X"
    ticker = yq.Ticker(texto_conversao)

    moeda_em_real = ticker.info["regularMarketPrice"]
    return moeda_em_real


def obtem_cotacoes(acoes):
    """
    Obtém as cotações das ações dadas.

    Recebe uma lista de códigos de ações, busca as cotações das ações utilizando a biblioteca yahooquery e retorna um dicionário ligando os códigos das ações com suas respectivas cotações.

    :param acoes: Lista dos códigos das ações
    :type acoes: list(str)
    :return: Um dicionário ligando as ações com suas cotações
    :rtype: dict(str, dict(str, Any))
    """
    texto_acoes = ' '.join(acoes)
    tickers_acoes = yq.Ticker(texto_acoes)

    dicionario_cotacoes = tickers_acoes.price

    return dicionario_cotacoes


def moedas_em_real(moedas):
    """
    Recebe uma lista de moedas e retorna os valores delas em reais.

    Recebe uma lista de códigos de moedas, busca os valores de conversão para
    real (BRL) utilizando a biblioteca yahooquery e retorna um dicionário ligando
    os códigos com seus respectivos valores de conversão para real.

    :param moedas: Lista de códigos de moedas
    :type moedas: list(str)
    :return: Dicionário ligando os códigos com os valores de conversão
    :rtype: dict(str, float)
    """
    textos_moedas = []
    for moeda in moedas:
        texto_conversao = f"{moeda}BRL=X"
        textos_moedas.append(texto_conversao)

    texto_conversoes = ' '.join(textos_moedas)
    tickers_moedas = yq.Tickers(texto_conversoes)
    dicionario_cotacoes = dict(tickers_moedas.tickers)

    dicionario_valor_real = {}
    for texto_conversao in dicionario_cotacoes.keys():
        ticker = dicionario_cotacoes[texto_conversao]
        moeda_em_real = ticker.info["regularMarketPrice"]

        moeda = texto_conversao[:-5]
        dicionario_valor_real[moeda] = moeda_em_real

    return dicionario_valor_real


def multiplica_cotacao(cotacao, razao):
    """
    Multiplica uma cotação por um valor.

    Multiplica os valores "Open", "High", "Low" e "Close" de uma cotação pela
    razão dada. Multiplicar a cotação diretamente resulta no volume vendido
    ("Volume") também sendo multiplicado, o que pode ser indesejado.

    :param cotacao: Cotação obtida de Ticker.history()
    :type cotacao: pandas.core.frame.DataFrame
    :param razao: Razão pela qual a cotação será multiplicada
    :type razao: float
    """
    cotacao["Open"] *= razao
    cotacao["High"] *= razao
    cotacao["Low"] *= razao
    cotacao["Close"] *= razao


def valor_carteira_reais(carteria):
    """
    Calcula o valor de uma carteira em reais.

    Busca os valores dos ativos que estão na carteira usando a biblioteca
    yahooquery, converte para reais e os soma. A carteira deve conter uma chave
    "moedas" com valor de um dicionário composto de chaves com o código das
    moedas e valores com a quantidade possuida. A carteira também deve conter
    uma chave "acoes" com valor de um dicionário composto de chaves com o
    código das ações e valores com a quantidade possuida.

    :param carteira: A carteira cujos ativos serão avaliados.
    :type carteira: dict(str, dict(str, float))
    :return: O valor da carteira em reais
    :rtype: int
    """
    moedas = carteria["moedas"]
    acoes = carteria["acoes"]

    cotacoes = obtem_cotacoes(acoes.keys(), 1)

    moedas_para_conversao = set(moedas.keys())
    for cotacao in cotacoes.values():
        moeda_da_cotacao = cotacao.info["currency"]
        moedas_para_conversao.add(moeda_da_cotacao)

    # Descarta BRL do set pois ele é a moeda para qual se está convertendo
    moedas_para_conversao.discard("BRL")
    moedas_para_real = moedas_em_real(moedas_para_conversao)
    moedas_para_real["BRL"] = 1

    total_reais = 0

    for moeda, quantidade in moedas:
        moeda_em_reais = quantidade * moedas_para_real[moeda]
        total_reais += moeda_em_reais

    for acao, cotacao in cotacoes:
        moeda_acao = cotacao.info["currency"]
        preco_original = cotacao.info["Close"]
        preco_convertido = preco_original * moedas_para_real[moeda_acao]

        acao_em_reais = preco_convertido * acoes[acao]
        total_reais += acao_em_reais

    return acao_em_reais