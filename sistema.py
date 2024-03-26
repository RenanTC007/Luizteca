from getpass import getpass
from hashlib import sha256
import datetime
from classes import *
import os
import json

SEM_PERMISSAO = "Você não tem permissão para realizar esta ação."

def clear(): # Limpa a tela.
    if os.name == "nt": os.system("cls")
    else: os.system("clear")

def fazer_login():
    print("Bem-vindo. Faça login, ou saia com o atalho CTRL+C.")
    while True:
        email = input("Digite seu e-mail: ")
        senha = sha256(getpass("Digite sua senha: ").encode()).hexdigest() # Lê a senha sem mostrar na tela com GETPASS e a criptografa com SHA256.

        funcionario_atual = 0
        for funcionario in funcionarios: # Procura um funcionário com o email digitado.
            if funcionario.email == email: funcionario_atual = funcionario

        if funcionario_atual == 0: # Se nenhum funcionário com este email foi encontrado.
            print("Este e-mail não está cadastrado. Tente novamente.")
        else:
            if funcionario_atual.senha == senha: 
                print("Logado com sucesso.")
                break # Volta pro loop inicial
            else: print("Senha incorreta. Tente novamente.")
    return funcionario_atual

def listar_publicacoes(nome=""):
    i = 1
    nome = nome.lower() # Não é case sensitive.
    for p in publicacoes:
        if nome in p.titulo.lower():
            print(f"[{i}] {p.titulo}, ISBN {p.isbn}")
        i += 1

def listar_funcionarios():
    i = 1
    for fun in funcionarios:
        print(f"[{i}] {fun.nome}, CPF {fun.cpf}")
    i += 1


def sistema(): # Chamado até sair da conta.
    print(f"Bem-vindo {funcionario_atual.nome}. Opções disponíveis: ")
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
    print("[11] Alterar dados de um funcionário.")
    print("[12] Listar exemplares emprestados.")
    print("[13] Multar exemplares não conservados.")
    
    print("[99] Sair da conta.")
    
    while True: # Tenta pegar uma escolha válida até conseguir.
        try:
            escolha = int(input("Escolha: "))
            break
        except:
            print("Você não digitou um número. Tente novamente.")

    match escolha:
        case 1:
            if e_dono:
                funcionarios.append(dono.cadastrar_funcionario()) # Adiciona o funcionário cadastrado na lista de funcionários.
            else:
                print(SEM_PERMISSAO) # Se não for dono, mostrar que não tem permissão.
        case 2:
            if e_dono:
                if len(funcionarios) == 1: 
                    print("Não há outros funcionários cadastrados.") # Apenas o dono está cadastrado.
                else:
                    funcionarios.remove(dono.remover_funcionario(funcionarios)) # Remove o funcionário escolhido.
            else:
                print(SEM_PERMISSAO)
        case 3:
            funcionario_atual.mudar_senha() # Função da classe Funcionario.
        case 4:
            clientes.append(funcionario_atual.cadastrar_cliente()) # Adiciona um cliente novo na lista de clientes.
        case 5:
            publicacoes.append(funcionario_atual.adicionar_publicacao()) # Adiciona uma publicação nova na lista de publicações.
        case 6:
            if len(publicacoes) == 0: # 0 publicações cadastradas, não dá para adicionar exemplares.
                print("Não há publicações cadastradas. Por favor, cadastre uma publicação primeiro.")
            else: 
                print("Adicionando um novo exemplar. Escolha um número correspondente à publicação que está sendo cadastrada:")
                listar_publicacoes()
                funcionario_atual.adicionar_exemplar(publicacoes)
        case 7:
            while True:
                try:
                    if len(publicacoes) == 0:
                        print("Nenhuma publicação no sistema.")
                        break
                    if len(clientes) == 0:
                        print("Não há clientes cadastrados.")
                        break
                    listar_publicacoes()
                    n = int(input("Escolha uma dessas publicações para emprestar: "))
                    if n < 1 or n > len(publicacoes): raise Exception() # Verifica se o número escolhido corresponde a uma publicação.

                    p = publicacoes[n-1] # -1 porque listamos as publicações a partir do 1.
                    if p.quantidade_exemplares_emprestados() == p.quantidade_exemplares(): # Todos foram emprestados.
                        print("Não há exemplares disponíveis para esta publicação.")
                        break
                    else:
                        # Pede-se o CPF por motivos de segurança: não é muito legal o funcionário ter acesso a todos os clientes.
                        cpf = int(input("Qual cliente quer pegar este título emprestado? Digite o CPF (com pontuação): "))
                        cliente = 0
                        for c in clientes: # Verifica todos os clientes em busca de um CPF.
                            if c.cpf == cpf: cliente = c
                        if cliente == 0:
                            print("O CPF digitado não foi encontrado. Certifique-se de digitar o CPF com pontuação.")
                            raise Exception()
                        for e in p.exemplares: # Procura nos exemplares da publicação e empresta um.
                            if e.emprestado == False:
                                e.emprestar_exemplar(funcionario_atual, datetime.datetime.now())
                                break
                        print(f"Exemplar de {p.titulo} emprestado para {cliente.nome} com sucesso no dia {datetime.datetime.now()} com sucesso.")
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

                    e = p.exemplares[n-1] # Exemplar escolhido.
                    estado = int(input("Qual é o estado de conservação deste exemplar?\n[1] Conservado.\n[2] Não conservado."))
                    if estado < 1 or estado > 2: raise Exception()

                    e.devolver_exemplar(datetime.datetime.now())
                    if estado == 2: 
                        print("Uma multa será aplicada ao cliente de acordo com o dono da biblioteca.")
                        print("Exemplar removido do sistema.")
                        multar.append([p, e]) # Anexa o exemplar e a publicação para o dono multar.
                        p.exemplares.remove(e)
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
                print("Os funcionários cadastrados são:")
                listar_funcionarios()
            else:
                print(SEM_PERMISSAO)
        case 11:
            if e_dono:
                listar_funcionarios()
                while True:
                    try:
                        n = int(input("Escolha um funcionário para alterar seus dados: "))
                        if n < 1 or n > len(funcionarios): raise Exception()
                        # Ainda precisamos programar isso
                    except:
                        print("Você digitou algo errado. Tente novamente.")
            else:
                print(SEM_PERMISSAO)
        case 12:
            print("Exemplares emprestados:")
            i = 1
            for p in publicacoes: # Procura nas publicações
                for e in p.exemplares(): # Procura nos exemplares
                    if e.emprestado:
                        print("[{i}] {p.tipo()} {p.titulo} ISBN {p.isbn}, emprestado por {e.funcionario} no dia {e.data_emprestimo}.")
                        i += 1
        case 13:
            if e_dono:
                print("Entre em contato com um dos clientes abaixo e dê baixa escolhendo uma das opções abaixo.")
                while True:
                    try:
                        i = 1
                        for m in multar:
                            p = m[0]
                            e = m[1]
                            print(f"[{i}] {p.tipo()} {p.titulo}, ISBN {p.isbn}, emprestado por {e.funcionario} para {e.cliente.nome} com CPF {e.cliente.cpf} e número de telefone {e.cliente.telefone}, emprestado no dia {e.data_emprestimo} e devolvido no dia {e.data_devolucao}.")
                        escolha = int(input("Qual dos exemplares você quer dar baixa? "))
                        if escolha < 1 or escolha > len(multar): raise Exception()
                        multar.remove(multar[n-1])
                        print("Sucesso.")
                    except:
                        print("Você digitou algo errado. Tente novamente.")
            else:
                print(SEM_PERMISSAO)
        case _:
            print("Você não digitou uma opção válida.")
    return escolha

def carregar_arquivo_funcionarios():
    f = open("funcionarios.json", "r")
    

# Cadastrando o dono com a senha padrão
dono = Dono("Luiz de Moraes Sampaio", "426.704.238-17", "Guarulhos", "(11) 96061-8848", "luiz.sagitario@yahoo.com.br", 2, SENHA_PADRAO)
funcionarios = [dono] # Primeiro funcionário cadastrado é o dono.
clientes = []
publicacoes = []
multar = []

# carregar_arquivo_funcionarios()

while True: # Loop do sistema
    funcionario_atual = fazer_login()
    e_dono = funcionario_atual == dono # A variável e_dono (é dono) diz se o funcionário logado é dono.
    while True:
        escolha_sistema = sistema()
        if escolha_sistema != 99: input("Aperte ENTER para continuar...")
        clear()
        if escolha_sistema == 99: break
