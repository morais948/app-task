from conexao import Conexao
import hashlib
import json

class Usuario(object):
    def __init__(self):
        self._dados_conexao = {'user': 'root', 'password': '', 
            'host': '127.0.0.1', 'database': 'app_tarefas_estacio'}
        self._conexao = Conexao(self._dados_conexao).conexao
        self._cursor = self._conexao.cursor()
        self._id = ''
        self._nome = ''
        self._email = ''
        self._senha = ''
        self._esta_logado = False

    def get_id(self):
        return self._id

    def get_nome(self):
        return self._nome

    def get_email(self):
        return self._email

    def get_logado(self):
        return self._esta_logado

    def _executar_comando(self, query="", dados="", salvar=False):
        self._cursor.execute(query, dados)
        if salvar:
            self._conexao.commit()
        
    def _criptografar_senha(self, senha):
        senha = hashlib.md5(senha.encode())
        senha_criptografada = senha.hexdigest()
        return senha_criptografada

    def cadastrar_usuario(self, nome, email, senha):
        try:
            senha = self._criptografar_senha(senha)
            query = "insert into usuarios (nome, email, senha) values(%s, %s, %s)"
            dados = (f'{nome}', f'{email}', f'{senha}')
            self._executar_comando(query, dados, True)
        except Exception as err:
            if '1062' in str(err):
                print('erro email existente')
            else:
                print(f'erro inesperado: {err}')

    def listar_usuarios(self):
        if self._esta_logado:
            query = 'select * from usuarios'
            lista = []
            self._executar_comando(query)
            for (id, nome, email, senha) in self._cursor:
                dic = {"id": id, "nome": nome, "email": email, "senha": senha}
                usuario_json = json.dumps(dic)
                lista.append(usuario_json)
            return lista
        else:
            return []

    def buscar_usuario(self, nome):
        if self._esta_logado:
            query = f"select * from usuarios u where u.nome like '%{nome}%'"
            self._executar_comando(query)
            lista = []
            for (id, nome, email, senha) in self._cursor:
                dic = {"id": id, "nome": nome, "email": email, "senha": senha}
                usuario_json = json.dumps(dic)
                lista.append(usuario_json)
            return lista
    
    def alterar_campo_usuario(self, campo, valor):
        if self._esta_logado:
            query = f'update usuarios u set {campo}=%s where u.id=%s'
            dados = (f'{valor}', f'{self._id}')
            self._executar_comando(query, dados, True)

    def deletar_usuario(self):
        if self._esta_logado:
            query = f'delete from usuarios where id={self._id}'
            self._executar_comando(query=query, salvar=True)
            self._esta_logado = False

    def fazer_login(self, email, senha):
        senha = self._criptografar_senha(senha)
        query = f'select * from usuarios u where u.email=%s and u.senha=%s'
        dados = (f'{email}', f'{senha}')
        self._executar_comando(query, dados)
        
        json_obj = self._retorna_json(self._cursor)
        if json_obj != None:
            useruario = json.loads(json_obj)
            self._id = useruario['id']
            self._nome = useruario['nome']
            self._email = useruario['email']
            self._senha = useruario['senha']
            self._esta_logado = True
            return json_obj
        else:
            return 'login ou senha invalidos'

    def _retorna_json(self, cursor):
        user = None
        for (id, nome, email, senha) in cursor:
            dic = {"id": id, "nome": nome, "email": email, "senha": senha}
            user = json.dumps(dic)
        return user

    def deslogar(self):
        self._cursor.close()
        self._conexao.close()

if __name__ == "__main__":
    user = Usuario()
    user.cadastrar_usuario('Matheus', 'matheusmorais948@gmail.com', '123')
    user.deslogar()
