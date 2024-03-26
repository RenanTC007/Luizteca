from getpass import getpass
from hashlib import sha256
import datetime
from classes import *
import os

def clear():
    os.system("clear")

def fazer_login():
    print("Bem-vindo. Faça login, ou saia com o atalho CTRL+C.")
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

def listar_publicacoes(nome=""):
    i = 1
    nome = nome.lower()
    for p in publicacoes:
        if nome in p.titulo.lower():
            print(f"[{i}] {p.titulo}, ISBN {p.isbn}")
        i += 1

def sistema():
    print("Bem-vindo,", funcionario_atual.nome, ". Opções disponíveis: ")
    print("[1] Cadastrar funcionário.")
    print("[2] Demitir funcionário.")
    print("[3] Mudar sua senha.")
    print("[4] Cadastrar cliente.")
    print("[5] Adicionar publicação.")
    print("[6] Adicionar exemplar.")
    print("[7] Emprestar exemplar.")
    print("[8] Devolver exemplar.")
    print("[9] Buscar publicação por título.")
    print("[10] Listar funcionários.")
    
    print("[99] Sair da conta.")
    
    while True:
        try:
            escolha = int(input("O que você deseja fazer? "))
            break
        except:
            print("Você não digitou um número. Tente novamente.")

    match escolha:
        case 1:
            if e_dono:
                funcionarios.append(dono.cadastrar_funcionario())
            else:
                print("Você não tem permissões para cadastrar funcionários.")
        case 2:
            if e_dono:
                if len(funcionarios) == 1: print("Não há outros funcionários cadastrados.")
                else: funcionarios.remove(dono.remover_funcionario(funcionarios))
            else:
                print("Você não tem permissão para remover funcionários.")
        case 3:
            funcionario_atual.mudar_senha()
        case 4:
            clientes.append(funcionario_atual.cadastrar_cliente())
        case 5:
            nova_publicacao = funcionario_atual.adicionar_publicacao()
            publicacoes.append(nova_publicacao)
        case 6:
            if len(publicacoes) == 0: print("Não há publicações cadastradas. Por favor, cadastre uma publicação primeiro.")
            else: 
                funcionario_atual.adicionar_exemplar(publicacoes)
        case 7:
            while True:
                try:
                    if len(publicacoes) == 0:
                        print("Nenhuma publicação no sistema.")
                        break
                    listar_publicacoes()
                    n = int(input("Escolha uma dessas publicações para emprestar: "))
                    if n < 1 or n > len(publicacoes): raise Exception()

                    p = publicacoes[n-1]
                    if p.quantidade_exemplares_emprestados() == p.quantidade_exemplares():
                        print("Não há exemplares disponíveis para esta publicação.")
                        break
                    else:
                        cpf = int(input("Qual cliente quer pegar este título emprestado? Digite o CPF (com pontuação): "))
                        cliente = 0
                        for c in clientes:
                            if c.cpf == cpf: cliente = c
                        if cliente == 0:
                            print("O CPF digitado não foi encontrado. Certifique-se de digitar o CPF com pontuação.")
                            raise Exception()
                        for e in p.exemplares:
                            if e.emprestado == False:
                                e.emprestar_exemplar(funcionario_atual)
                                break
                        print(f"Exemplar de {p.titulo} emprestado para {cliente.nome} com sucesso.")
                        break
                except:
                    print("Você digitou um número fora do intervalo permitido ou não digitou um número. Tente novamente.")
        case 8:
            while True:
                try:
                    if len(publicacoes) == 0:
                        print("Nenhuma publicação no sistema.")
                        break
                    listar_publicacoes()
                    n = int(input("Digite o número da publicação que está sendo devolvida: "))
                    if n < 1 or n > len(publicacoes): raise Exception()
                    if p.quantidade_exemplares_emprestados() == 0:
                        print("Nenhum exemplar desta publicação foi emprestado.")
                        break
                    p = publicacoes[n-1]
                    p.listar_exemplares_emprestados()
                    n = int(input("Selecione um dos exemplares emprestados para devolver: "))
                    if n < 1 or n > p.quantidade_exemplares_emprestados():
                        raise Exception()
                    e = p.exemplares[n-1]
                    e.devolver_exemplar(datetime.datetime.now())
                    print("Exemplar devolvido em", datetime.datetime.now(),"com sucesso.")
                    break
                except:
                    print("Você digitou um número fora do intervalo permitido ou não digitou um número. Tente novamente.")
        case 9:
            nome = input("Digite parte do nome da publicação: ")
            print("Publicações encontradas: ")
            listar_publicacoes(nome)
        case 10:
            if e_dono:
                # Listar funcionários aqui.
                pass
            else:
                print("Você não tem permissão para realizar esta ação.")
        case _:
            print("Você não digitou uma opção válida.")
    return escolha

# Cadastrando o dono com a senha padrão
dono = Dono("Luiz de Moraes Sampaio", "426.704.238-17", "Guarulhos", "(11) 96061-8848", "luiz.sagitario@yahoo.com.br", 2, SENHA_PADRAO)
funcionarios = [dono]
clientes = []
publicacoes = []

while True:
    funcionario_atual = fazer_login()
    e_dono = funcionario_atual == dono
    while True:
        escolha_sistema = sistema()
        if escolha_sistema != 99: input("Aperte ENTER para continuar...")
        clear()
        if escolha_sistema == 99: break
