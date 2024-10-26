'''

   . o computador (ou seja, seu programa) deve jogar usando 'X's;
   . o usuário (por exemplo, você) deve jogar usando 'O's;
   . o primeiro movimento pertence ao computador - ele sempre 
    coloca seu primeiro 'X' no meio do quadro;
   . todos os quadrados são numerados linha por linha, começando 
    com 1 (consulte a sessão de exemplo abaixo para referência)
   . o usuário insere seu movimento inserindo o número do quadrado 
    escolhido - o número deve ser válido, ou seja, deve ser um número 
    inteiro, deve ser maior que 0 e menor que 10, e não pode apontar 
    para um campo que já está ocupada;
   . o programa verifica se o jogo acabou - há quatro veredictos 
    possíveis: o jogo deve continuar, o jogo termina com um empate, 
    você ganha ou o computador ganha;
   . o computador responde seu movimento e a verificação é repetida;
   . não implementem qualquer forma de inteligência artificial - uma 
    escolha de campo aleatória feita pelo computador é boa o suficiente 
    para o jogo.

'''
import os
if os.name == 'nt':
    os.system('cls')

from random import randrange

# FUNÇÕES
def ocupado():
    print("\n------\nEssa casa está ocupada!\n------\n")
    print(0/0)

def ocupadopc():
    print(0/0)

def jogar():
    global casa
    play = 0
    while play == 0:
        try:
            casa = int(input("Casa de número: "))

            if casa <= 3: # ATÉ TRÊS
                if lista[0][casa - 1] == 'O' or lista[0][casa - 1] == 'X':
                    ocupado()
                else:
                    lista[0][casa - 1] = 'O'

            elif casa <= 6: #ATÉ  SEIS
                if lista[1][casa - 4] == 'O' or lista[1][casa - 4] == 'X':
                    ocupado()
                else:    
                    lista[1][casa - 4] = 'O'

            else: #ATÉ NOVE
                if lista[2][casa - 7] == 'O' or lista[2][casa - 7] == 'X':
                    ocupado()
                else:
                    lista[2][casa - 7] = 'O'
            print()        
            print("Você jogou na casa",casa)
            play = 1
        except:
            print("As casas podem apenas serem números inteiros de 1 a 9!")


def tabuleiro():
    print()
    for x in range(3):
        print(lista[0][x],end="|")
    print()
    for x in range(3):
        print(lista[1][x],end="|")
    print()
    for x in range(3):
        print(lista[2][x],end="|")
    print()

def computador():
    pc = 0
    while pc == 0:
        casa = randrange(1,10)

        try:
            if casa <= 3: # ATÉ TRÊS
                if lista[0][casa - 1] == 'O' or lista[0][casa - 1] == 'X':
                    ocupadopc()
                else:
                    lista[0][casa - 1] = 'X'

            elif casa <= 6: #ATÉ  SEIS
                if lista[1][casa - 4] == 'O' or lista[1][casa - 4] == 'X':
                    ocupadopc()
                else:    
                    lista[1][casa - 4] = 'X'

            else: #ATÉ NOVE
                if lista[2][casa - 7] == 'O' or lista[2][casa - 7] == 'X':
                    ocupadopc()
                else:
                    lista[2][casa - 7] = 'X'
            
            print()
            print("O computador jogou na casa", casa)
            pc = 1
        
        except:
            None
    




#JOGO - Verificar se alguém ganhou

def ganhar():
    global vencedor 
    global jogando
    for x in range(3):
    # JOGADOR
        # VERTICAL E HORIZONTAL
        if 'O' == lista[x][0] and 'O' == lista[x][1] and 'O' == lista[x][2]:
            vencedor = 'jogador'
            jogando = False
            return

        elif 'O' == lista[0][x] and 'O' == lista[1][x] and 'O' == lista[2][x]:
            vencedor = 'jogador'
            jogando = False
            return

        # DIAGONAL
    if 'O' == lista[0][0] and 'O' == lista[1][1] and 'O' == lista[2][2]:
        vencedor = 'jogador'
        jogando = False
        return

    elif 'O' == lista[0][2] and 'O' == lista[1][1] and 'O' == lista[2][0]:
        vencedor = 'jogador'
        jogando = False
        return

    # COMPUTADOR
    for x in range(3):

        # VERTICAL E HORIZONTAL
        if 'X' == lista[x][0] and 'X' == lista[x][1] and 'X' == lista[x][2]:
            vencedor = 'computador'
            jogando = False
            return

        elif 'X' == lista[0][x] and 'X' == lista[1][x] and 'X' == lista[2][x]:
            vencedor = 'computador'
            jogando = False
            return

        # DIAGONAL
    if 'X' == lista[0][0] and 'X' == lista[1][1] and 'X' == lista[2][2]:
        vencedor = 'computador'
        jogando = False
        return

    elif 'X' == lista[0][2] and 'X' == lista[1][1] and 'X' == lista[2][0]:
        vencedor = 'computador'
        jogando = False
        return



# JOGO
lista = [[1,2,3],[4,5,6],[7,8,9]]

print("Que comecem os jogos!\n O computador começa o jogo, ele usará X e você O.")

lista[1][1] = 'X'

tabuleiro()

jogando = True
vencedor = ''

pc = 0
play = 0

for x in range(4):
    if jogando == False:
        break
    print("\nAgora escolha a casa do seu próximo movimento!")
    jogar()
    ganhar()
    computador()
    ganhar()
    tabuleiro()
    print("--------------------------------------")


if jogando == True:
    print("Empate!")
else:
    print("++ O vencedor é o", vencedor,"++")
