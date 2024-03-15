from getpass import getpass
from hashlib import sha256
from classes import *

SENHA_PADRAO = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3" # 123
TETO_SALARIAL = 10000

def fazer_login():
    print("Bem-vindo. Faça login:")
    condicao = True
    while condicao:
        email = input("Digite seu e-mail: ")
        senha = sha256(getpass("Digite sua senha: ").encode()).hexdigest()

        funcionario_atual = 0
        for funcionario in funcionarios:
            if funcionario.email == email: funcionario_atual = funcionario

        if funcionario_atual == 0:
            print("Este e-mail não está cadastrado. Tente novamente.")
        else:
            if funcionario_atual.senha == senha: 
                print("Logado com sucesso.")
                condicao = False
            else: print("Senha incorreta. Tente novamente.")
    
def sistema():
    print("Bem-vindo,", funcionario_atual.nome, ", o que deseja fazer?")
    print("[1] Cadastrar funcionário.")
    escolha = 0
    condicao = True
    while condicao:
        try:
            escolha = int(input("O que você deseja fazer?"))
            condicao = (escolha < 1 or escolha > 9)
            if condicao: raise Exception()
        except:
            print("Você digitou uma opção inválida. Tente novamente.")

    match escolha:
        case 1:
            if funcionario_atual == dono: 
                condicao = True
                while condicao:
                    try:
                        print("Cadastrando um novo funcionário.")
                        nome = input("Nome: ")
                        cpf = input("Cpf: ")
                        endereco = input("Endereço: ")
                        telefone = input("Número de telefone: ")
                        email = input("E-mail: ")
                        salario = float(input("Salário [apenas números]: "))
                        senha = SENHA_PADRAO
                    except:
                        print("O salário deve ser um número menor que", TETO_SALARIAL, " Tente novamente.")

            else:
                print("Você não tem permissões para cadastrar funcionários.")


# Cadastrando o dono com a senha padrão
funcionario_atual = 0
dono = Dono("Luiz de Moraes Sampaio", "426.704.238-17", "Guarulhos", "(11) 94318-6452", "luiz.sampaio@yahoo.com.br", 2, SENHA_PADRAO)
funcionarios = [dono]

# Primeiro login (dono)
fazer_login()
sistema()