import mysql.connector
from mysql.connector import errorcode

class Conexao(object):
    def __init__(self, objeto_conexao):    
        try:
            self.conexao = mysql.connector.connect(**objeto_conexao)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Usuario ou senha invalidos')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('Banco de dados não existente')
            else:
                print(f'erro inesperado: {err}')

