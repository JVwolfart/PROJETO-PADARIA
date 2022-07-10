import sqlite3
from sqlite3.dbapi2 import connect
        
    

class Usuarios():
    def __init__(self):
       self.id = None
       self.nome = None
       self.senha = None
       self.criar = None
       self.editar = None
       self.excluir = None
       self.root = None
    
    def banco_para_modelo(self, usuario_banco):
        self.id = usuario_banco[0][0]
        self.nome = usuario_banco[0][1]
        self.senha = usuario_banco[0][2]
        self.criar = usuario_banco[0][3]
        self.editar = usuario_banco[0][4]
        self.excluir = usuario_banco[0][5]
        self.root = usuario_banco[0][6] 

class Funcionario():
    def __init__(self):
        self.id = None
        self.nome = None
        self.funcao = None
        self.matricula = None

class Cliente():
    def __init__(self):
        self.id = None
        self.nome = None


class Produto():
    def __init__(self):
        self.codigo = None
        self.nome = None
        self.valor = 0

class NFiscal():
    def __init__(self):
        self.num = None
        self.data = None
        self.id_func = None
        self.id_cliente = None
        self.valor = 0
        self.status = 'P'