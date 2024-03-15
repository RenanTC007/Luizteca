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
