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

class Dono(Funcionario):
    def __init__(self, nome, cpf, endereco, telefone, email, salario, senha):
        super().__init__(nome, cpf, endereco, telefone, email, salario, senha)
    
    def cadastrar_funcionario():
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

class Publicacao:
    def __init__(self, autor, editora, ano, titulo, genero, isbn):
        self.autor = autor
        self.editora = editora
        self.ano = ano
        self.titulo = titulo
        self.genero = genero
        self.isbn = isbn

class Livro(Publicacao):
    def __init__(self, autor, editora, ano, titulo, genero, isbn, volume):
        super().__init__(autor, editora, ano, titulo, genero, isbn)
        self.volume = volume

class Revista(Publicacao):
    def __init__(self, autor, editora, ano, titulo, genero, isbn, semana):
        super().__init__(autor, editora, ano, titulo, genero, isbn)
        self.semana = semana

class Jornal(Publicacao):
    def __init__(self, autor, editora, ano, titulo, genero, isbn, dia):
        super().__init__(autor, editora, ano, titulo, genero, isbn)
        self.dia = dia
