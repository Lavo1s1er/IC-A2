import requests
from bs4 import BeautifulSoup

def buscar_site(url):
    """Retorna o site da url parseado usando BS4 e lxml

    :param url: URL do site
    :type url: str
    :return: Informações do site parseadas com BS4 e lxml
    :rtype: bs4.BeautifulSoup
    """    
    resposta = requests.get(url)
    site = BeautifulSoup(resposta.text, "lxml")

    return site

def encontrar_div_com_classe(conteudo, classe):
    """Retorna o primeiro div com a classe especificada

    :param conteudo: De onde será obtido o div
    :type conteudo: bs4.BeautifulSoup
    :param classe: A classe que o div deve ter
    :type classe: str
    :return: O primeiro div encontrado que tenha a classe
    :rtype: bs4.element.Tag
    """    
    return conteudo.find("div", class_ = classe)

def ler_table_data(conteudo):
    """Retorna um dicionário com o conteúdo de todas tags 'td'

    As strings de todas as tags 'td' encontradas no parâmetro são agrupadas em
    pares chave-valor de um dicionário na ordem que forem encontradas. O parâmetro deve ter um número par de tags 'td' e cada segunda tag deve conter uma string que possa ser convertida em float.

    :param conteudo: Onde serão buscadas as tags 'td'
    :type conteudo: bs4.element.Tag
    :return: O dicionário com o conteúdo das tags 'td'
    :rtype: dict(str, float)
    """    
    celulas = conteudo.find_all("td")
    dicionario = {}

    iterador = iter(celulas)
    for celula in iterador:
        dicionario[celula.string] = float(next(iterador).string)
    
    return dicionario

def ler_ativos(conteudo):
    div_moedas = encontrar_div_com_classe(conteudo, "moeda")
    moedas = ler_table_data(div_moedas)

    div_acoes = encontrar_div_com_classe(conteudo, "acao")
    acoes = ler_table_data(div_acoes)

    ativos = {"moedas": moedas, "acoes": acoes}
    return ativos

def buscar_carteira(url):
    site = buscar_site(url)
    carteira = ler_ativos(site)
    return carteira