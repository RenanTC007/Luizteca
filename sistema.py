from getpass import getpass
from hashlib import sha256
from classes import *

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
    return funcionario_atual
    
def sistema():
    print("Bem-vindo,", funcionario_atual.nome, ". Opções disponíveis: ")
    print("[1] Cadastrar funcionário.")
    print("[2] Demitir funcionário.")
    print("[99] Sair da conta.")
    condicao = True
    while condicao:
        try:
            escolha = int(input("O que você deseja fazer? "))
            condicao = (escolha < 1 or escolha > 99)
            if condicao: raise Exception()
        except:
            print("Você digitou uma opção inválida. Tente novamente.")

    match escolha:
        case 1:
            if funcionario_atual == dono:
                funcionarios.append(dono.cadastrar_funcionario())
            else:
                print("Você não tem permissões para cadastrar funcionários.")
    
    return escolha

# Cadastrando o dono com a senha padrão
dono = Dono("Luiz de Moraes Sampaio", "426.704.238-17", "Guarulhos", "(11) 94318-6452", "luiz.sampaio@yahoo.com.br", 2, SENHA_PADRAO)
funcionarios = [dono]

while True:
    funcionario_atual = fazer_login()
    while True:
        escolha_sistema = sistema()
        if escolha_sistema == 99: break