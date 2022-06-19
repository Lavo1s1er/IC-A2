import cria_excel as ce
import graficos as gr


def mostrar_menu():
    titulo = '\nO' + ' Selecione uma opção '.center(38, '-') + 'O'
    opcoes = ['Avaliar carteira', 'Sair']
    parte_inferior = 'O' + '-' * 38 + 'O'

    print(titulo)

    for num, opcao in enumerate(opcoes):
        numero_da_opcao = num + 1
        linha = f'| {numero_da_opcao}. ' + opcao.ljust(34) + '|'
        print(linha)
    
    print(parte_inferior)

def avalia_carteira(url):
    ce.criar_excel(url)

    dias = 200

    gr.gerar_grafico_moedas(url, dias)
    gr.gerar_grafico_acoes(url, dias)
    gr.gerar_grafico_carteira(url, dias)

def iniciar_interface():
    resposta = -1

    while resposta != '2':
        mostrar_menu()

        resposta = input('Escolha: ')

        match resposta:
            case '1':
                url = input('Digite a URL do site com a carteira: ')
                avalia_carteira(url)
            case '2':
                print('Encerrando programa...')

if __name__ == '__main__':
    iniciar_interface()