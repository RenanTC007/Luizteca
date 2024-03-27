from getpass import getpass
from hashlib import sha256

SENHA_PADRAO = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3" # 123
TETO_SALARIAL = 10000 # Máximo valor que um funcionário pode ter de salário.

class Pessoa:
    def __init__(self, nome, cpf, endereco, telefone, email):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco
        self.telefone = telefone
        self.email = email

    def __str__(self):
        return f"Nome: {self.nome}\nCPF: {self.cpf}\nEndereço: {self.endereco}\nTelefone: {self.telefone}\nE-mail: {self.email}"

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
        # Retorna um objeto Pessoa com os dados acima.
        return Pessoa(nome, cpf, endereco, telefone, email)
    
    def mudar_senha(self):
        print("Mudando sua senha.")
        # Muda a senha usando GETPASS para esconder a senha e SHA256 para criptografar.
        self.senha = sha256(getpass("Digite uma nova senha: ").encode()).hexdigest()

    def adicionar_publicacao(self):
        while True:
            print("Adicionando uma nova publicação.")
            try:
                tipo = int(input("Escolha o tipo da publicação. Digite 1 para LIVRO, 2 para REVISTA e 3 para JORNAL: "))
                if tipo < 1 or tipo > 3: raise Exception() # Jogar um erro de o tipo não estiver entre 1 e 3.
                titulo = input("Título: ")
                autor = input("Autor: ")
                editora = input("Editora: ")
                edicao = int(input("Edição (apenas números inteiros): "))
                ano = int(input("Ano de publicação (apenas números inteiros): "))
                qntd = int(input("Quantidade de exemplares (apenas números inteiros): "))
                genero = input("Gênero: ")
                isbn = input("ISBN: ")
                break
            except:
                print("Você digitou algo errado. Tente novamente.")
        # Retorna um objeto de acordo com o tipo escolhido.
        match tipo:
            case 1:
                volume = input("Volume: ")
                return Livro(autor, editora, edicao, ano, titulo, genero, isbn, qntd, volume)
            case 2:
                semana = input("Semana: ")
                return Revista(autor, editora, edicao, ano, titulo, genero, isbn, qntd, semana)
            case 3:
                dia = input("Dia: ")
                return Jornal(autor, editora, edicao, ano, titulo, genero, isbn, qntd, dia)
        print("Nova publicação adicionada com sucesso. Agora adicione exemplares desta publicação.")

    def adicionar_exemplar(self, lista):
        while True:
            try:
                n = int(input())
                if n < 1 or n > len(lista): raise Exception() # A publicação deve estar na lista de publicações.
            except:
                print(f"Digite um número inteiro entre 1 e {len(lista)}. Tente novamente.")
            try:
                qntd = int(input("Digite a quantidade de exemplares a serem adicionados: "))
                if qntd < 1: raise Exception()
                break
            except:
                print("Digite um número inteiro positivo.")
        p = lista[n-1]
        p.adicionar_exemplar(qntd)
        print(f"{qntd} exemplar(es) do {p.tipo()} {p.titulo} adicionado(s) com sucesso.")

    def __str__(self):
        return super().__str__() + f"\nSalário: R${self.salario}"

class Dono(Funcionario):
    def __init__(self, nome, cpf, endereco, telefone, email, salario, senha):
        super().__init__(nome, cpf, endereco, telefone, email, salario, senha)
    
    def cadastrar_funcionario(self, funcionarios):
        while True:
            try:
                print("Cadastrando um novo funcionário.")
                nome = input("Nome: ")
                cpf = input("CPF (com pontuação): ")
                endereco = input("Endereço: ")
                telefone = input("Número de telefone: ")
                email = input("E-mail: ")
                for fun in funcionarios:
                    if email == fun.email:
                        print("Este e-mail já está cadastrado.")
                        raise Exception()
                salario = float(input("Salário [apenas números]: "))
                if salario > TETO_SALARIAL:
                    print(f"O salário deve ser um número menor que {TETO_SALARIAL}.")
                    raise Exception()
                senha = SENHA_PADRAO
                print("Funcionário", nome, "cadastrado com sucesso. A senha padrão é 123.")
                return Funcionario(nome, cpf, endereco, telefone, email, salario, senha) # Retorna um objeto Funcionário
            except:
                print(f"Tente novamente.")
    
    def remover_funcionario(self, lista_funcionarios):
        while True:
            cpf = input("Digite o CPF do funcionário que você quer demitir: ")
            for funcionario in lista_funcionarios: # Procura em todos os funcionários na lista.
                if funcionario != self: # Não pode demitir o dono.
                    if funcionario.cpf == cpf: 
                        print("Funcionário", funcionario.nome, "demitido com sucesso.")
                        return funcionario # Retorna o funcionário para ser removido da lista no sistema.py
            print("Nenhum funcionário encontrado com esse CPF. Tente novamente.")

class Publicacao:
    def __init__(self, autor, editora, edicao, ano, titulo, genero, isbn, qntd_exemplares):
        self.autor = autor
        self.editora = editora
        self.edicao = edicao
        self.ano = ano
        self.titulo = titulo
        self.genero = genero
        self.isbn = isbn
        self.exemplares = [] # Lista de exemplares desta publicação.
        self.adicionar_exemplar(qntd_exemplares)
        
    def quantidade_exemplares(self):
        return len(self.exemplares)

    def quantidade_exemplares_emprestados(self):
        i = 0
        for e in self.exemplares:
            if e.emprestado: i += 1
        return i

    def tipo(self):
        pass # Retorna o tipo da publicação. Sobrescrever esta função nas classes derivadas.

    def listar_exemplares_emprestados(self):
        i = 1
        for e in self.exemplares:
            if e.emprestado:
                print(f"[{i}] Emprestado para {e.cliente.nome} no dia {e.data_emprestimo} por {e.funcionario.nome} (CPF {e.funcionario.cpf}).")
                i += 1

    def adicionar_exemplar(self, qntd):
        for i in range(qntd):
            self.exemplares.append(Exemplar()) # Adiciona um novo objeto Exemplar à publicação.

    def __str__(self):
        return f"Autor: {self.autor}\nEditora: {self.editora}\nEdição: {self.edicao}\nAno: {self.ano}\nTítulo: {self.titulo}\nGênero: {self.genero}\nISBN: {self.isbn}"

class Livro(Publicacao):
    def __init__(self, autor, editora, edicao, ano, titulo, genero, isbn, qntd, volume):
        super().__init__(autor, editora, edicao, ano, titulo, genero, isbn, qntd)
        self.volume = volume

    def tipo(self):
        return "Livro"

    def __str__(self):
        return super().__str__() + f"\nVolume: {self.volume}"

class Revista(Publicacao):
    def __init__(self, autor, editora, edicao, ano, titulo, genero, isbn, qntd, semana):
        super().__init__(autor, editora, edicao, ano, titulo, genero, isbn, qntd)
        self.semana = semana

    def tipo(self):
        return "Revista"

    def __str__(self):
        return super().__str__() + f"\nSemana: {self.semana}"
        
class Jornal(Publicacao):
    def __init__(self, autor, editora, edicao, ano, titulo, genero, isbn, qntd, dia):
        super().__init__(autor, editora, edicao, ano, titulo, genero, isbn, qntd)
        self.dia = dia

    def tipo(self):
        return "Jornal"

    def __str__(self):
        return super().__str__() + f"\nDia: {self.dia}"

class Exemplar: # Cada publicação tem uma lista de exemplares com objetos desta classe. Assim é possível ter vários exemplares de uma mesma publicação.
    def __init__(self):
        self.emprestado = False
        self.cliente = None
    def emprestar_exemplar(self, funcionario, cliente, data_emprestimo):
        self.funcionario = funcionario
        self.emprestado = True
        self.cliente = cliente
        self.data_emprestimo = data_emprestimo
    def devolver_exemplar(self, data_devolucao):
        self.data_devolucao = data_devolucao
        self.emprestado = False
