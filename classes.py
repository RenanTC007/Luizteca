from getpass import getpass
from hashlib import sha256

SENHA_PADRAO = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3" # 123
TETO_SALARIAL = 10000

class Pessoa:
    def __init__(self, nome, cpf, endereco, telefone, email):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco
        self.telefone = telefone
        self.email = email

class Funcionario(Pessoa):
    def __init__(self, nome, cpf, endereco, telefone, email, salario, senha):
        super().__init__(nome, cpf, endereco, telefone, email)
        self.salario = salario
        self.senha = senha

    def cadastrar_cliente(self):
        print("Cadastrando um novo cliente.")
        nome = input("Nome: ")
        cpf = input("CPF: ")
        endereco = input("Endereço: ")
        telefone = input("Telefone: ")
        email = input("E-mail: ")
        return Pessoa(nome, cpf, endereco, telefone, email)
    
    def mudar_senha(self):
        print("Mudando sua senha.")
        self.senha = sha256(getpass("Digite uma nova senha: ").encode()).hexdigest()

    def adicionar_publicacao(self):
        while True:
            print("Adicionando uma nova publicação.")
            try:
                tipo = int(input("Tipo da publicação. Digite 1 para LIVRO, 2 para REVISTA e 3 para JORNAL: "))
                if tipo < 1 or tipo > 3: raise Exception()
                autor = input("Autor: ")
                editora = input("Editora: ")
                ano = int(input("Ano de publicação: "))
                titulo = input("Título: ")
                genero = input("Gênero: ")
                isbn = input("ISBN: ")

                break
            except:
                print("Você digitou algo errado. Tente novamente.")
        match tipo:
            case 1:
                volume = input("Volume: ")
                return Livro(autor, editora, ano, titulo, genero, isbn, volume)
            case 2:
                semana = input("Semana: ")
                return Revista(autor, editora, ano, titulo, genero, isbn, semana)
            case 3:
                dia = input("Dia: ")
                return Jornal(autor, editora, ano, titulo, genero, isbn, dia)
        print("Nova publicação adicionada com sucesso. Agora adicione exemplares desta publicação.")

    def adicionar_exemplar(self, lista):
        print("Adicionando um novo exemplar. Escolha um número correspondente à publicação que está sendo cadastrada:")
        i = 1
        for p in lista:
            print(f"[{i}] {p.titulo}, ISBN {p.isbn}, {p.tipo()}.")
            i += 1
        n = 0
        while True:
            try:
                n = int(input())
                if n < 1 or n > len(lista): raise Exception()
                break
            except:
                print(f"Digite um número inteiro entre 1 e {len(lista)}. Tente novamente.")
                pass
        lista[n-1].exemplares.append(Exemplar())
        print(f"Exemplar do {lista[n-1].tipo()} {lista[n-1].titulo} adicionado com sucesso.")
        

class Dono(Funcionario):
    def __init__(self, nome, cpf, endereco, telefone, email, salario, senha):
        super().__init__(nome, cpf, endereco, telefone, email, salario, senha)
    
    def cadastrar_funcionario(self):
        while True:
            try:
                print("Cadastrando um novo funcionário.")
                nome = input("Nome: ")
                cpf = input("Cpf: ")
                endereco = input("Endereço: ")
                telefone = input("Número de telefone: ")
                email = input("E-mail: ")
                salario = float(input("Salário [apenas números]: "))
                senha = SENHA_PADRAO
                print("Funcionário", nome, "cadastrado com sucesso. A senha padrão é 123")
                return Funcionario(nome, cpf, endereco, telefone, email, salario, senha)
            except:
                print("O salário deve ser um número menor que", TETO_SALARIAL, " Tente novamente.")
    
    def remover_funcionario(self, lista_funcionarios):
        while True:
            cpf = input("Digite o CPF do funcionário que você quer demitir: ")
            for funcionario in lista_funcionarios:
                if funcionario.cpf == cpf: 
                    print("Funcionário", funcionario.nome, "demitido com sucesso.")
                    return funcionario
            print("Nenhum funcionário encontrado com esse CPF. Tente novamente.")

class Publicacao:
    def __init__(self, autor, editora, ano, titulo, genero, isbn):
        self.autor = autor
        self.editora = editora
        self.ano = ano
        self.titulo = titulo
        self.genero = genero
        self.isbn = isbn
        self.exemplares = []

    def quantidade_exemplares(self):
        return len(self.exemplares)

    def tipo(self):
        pass

class Livro(Publicacao):
    def __init__(self, autor, editora, ano, titulo, genero, isbn, volume):
        super().__init__(autor, editora, ano, titulo, genero, isbn)
        self.volume = volume

    def tipo(self):
        return "Livro"

class Revista(Publicacao):
    def __init__(self, autor, editora, ano, titulo, genero, isbn, semana):
        super().__init__(autor, editora, ano, titulo, genero, isbn)
        self.semana = semana

    def tipo(self):
        return "Revista"

class Jornal(Publicacao):
    def __init__(self, autor, editora, ano, titulo, genero, isbn, dia):
        super().__init__(autor, editora, ano, titulo, genero, isbn)
        self.dia = dia

    def tipo(self):
        return "Jornal"

class Exemplar:
    def __init__(self):
        self.emprestado = False
    def emprestar_exemplar(self, funcionario):
        self.funcionario = funcionario
        self.emprestado = True
    def devolver_exemplar(self, data_devolucao):
        self.data_devolucao = data_devolucao
        self.emprestado = False
