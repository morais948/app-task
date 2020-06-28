import usuario
from conexao import Conexao
import json
import re

class Grupo(object):
    def __init__(self):
        self._dados_conexao = {'user': 'root', 'password': '', 
            'host': '127.0.0.1', 'database': 'app_tarefas_estacio'}
        self._conexao = Conexao(self._dados_conexao).conexao
        self._cursor = self._conexao.cursor()

    def _executar_comando(self, query="", dados="", salvar=False):
        self._cursor.execute(query, dados)
        if salvar:
            self._conexao.commit()

    def criar_grupo(self, nome, descricao, participantes):
        query = "insert INTO grupos(nome_grupo, descricao, ids_participante)VALUES(%s, %s, %s)"
        dados = (f'{nome}', f'{descricao}', f'{participantes}')
        self._executar_comando(query, dados, True)

    def pesquisar_grupos(self, id):
        query = f"select g.* from grupos g where g.ids_participante like '%{id}%' "
        self._executar_comando(query)
        lista = []
        for (id, nome_grupo, descricao, data_criacao, participantes) in self._cursor:
            dic = {"id": id, "nome_grupo": nome_grupo, 
                    "descricao": descricao, "data_criacao": data_criacao, 'participantes': participantes}
            lista.append(dic)
        return lista

    def pegar_informacoes(self, id):
        query = f"SELECT g.nome_grupo, g.descricao, g.data_criacao from grupos g where g.id = {id}"
        self._executar_comando(query)
        dic = None
        for (nome_grupo, descricao, data_criacao) in self._cursor:
            dic = {"nome_grupo": nome_grupo,
                    "descricao": descricao, "data_criacao": data_criacao.strftime('%d/%m/%Y')}
        return dic

    def listar_participantes(self, id_grupo):
        query = f"select g.ids_participante from grupos g where g.id = {id_grupo}"
        self._executar_comando(query)
        ids = None
        for (id) in self._cursor:
            for i in id:
                ids = i
        
        lista = []
        query = f"select u.nome from usuarios u where u.id in ({ids})"
        self._executar_comando(query)
        for (nome) in self._cursor:
            dic = {"nome": nome[0]}
            lista.append(dic)
        return lista

    def get_tarefas(self, id_grupo):
        query = f"SELECT t.id, t.id_responsavel, t.nome_tarefa, u.nome, t.dta_feita, t.descricao FROM tarefas t join grupos g on t.id_grupo = g.id join usuarios u on t.id_responsavel = u.id where g.id = {id_grupo}"
        self._executar_comando(query)
        lista = []
        for (id, id_responsavel, nome_tarefa, nome, dta_feita, descricao) in self._cursor:
            if dta_feita != None:
                dta_feita = 'feita'
            else:
                dta_feita = 'por fazer'
            dic = {"id_tarefa": id, "id_responsavel": id_responsavel, "nome": nome_tarefa, "responsavel": nome, "status": dta_feita, "descricao": descricao}
            lista.append(dic)
        return lista

    def get_integrantes(self, id_grupo):
        query_participantes = f"SELECT g.ids_participante from grupos g WHERE g.id = {id_grupo}"
        self._executar_comando(query_participantes)
        lista_participantes = []
        for (ids) in self._cursor:
            for i in ids:
                if len(i.split(',')) == 1:
                    lista_participantes = i
                else:
                    lista_participantes = i.split(',')
                    lista_participantes = ','.join(lista_participantes)
        dados = lista_participantes
        
        query_final = f"SELECT u.id, u.nome from usuarios u WHERE u.id in({dados})"
        self._executar_comando(query_final)
        lista = []
        for (id_responsavel, nome) in self._cursor:
            dic = {"id_responsavel": id_responsavel, "nome": nome}
            lista.append(dic)
        return lista
    
    def inserir_participante(self, id_grupo, id_user):        
        query_0 = f"select * from usuarios u where u.id = {id_user}"
        self._executar_comando(query_0)
        user = None
        for i in self._cursor:
            user = i
        if user:
            query = f"SELECT * from grupos g WHERE g.ids_participante like '%{id_user}%' and g.id = {id_grupo}"
            self._executar_comando(query)
            ja_existe = None
            for i in self._cursor:
                ja_existe = i
            if ja_existe != None:
                return 'usuário já está no grupo'

            query_1 = f"select g.ids_participante from grupos g where g.id = {id_grupo}"
            self._executar_comando(query_1)
            participantes = None
            for x in self._cursor:
                participantes = x[0]

            query_2 = "UPDATE grupos SET ids_participante = %s where id = %s"
            dados = (f'{participantes + "," + str(id_user)}', f'{id_grupo}')
            self._executar_comando(query_2, dados, True)
            return 'usuário adicionado!'
        else:
            return 'usuário inválido'
        

    def excluir_participante(self, id_grupo, id_user):
        query_1 = f"select g.ids_participante from grupos g where g.id = {id_grupo}"
        self._executar_comando(query_1)
        participantes = None
        for x in self._cursor:
            participantes = x[0]

        if ',' in participantes:
            if re.findall(f',?{id_user},?', participantes)[0][0] == ',' and re.findall(f',?{id_user},?', participantes)[0][-1] == ',':
                participantes = participantes.replace(f'{id_user},', '')
            elif re.findall(f',?{id_user},?', participantes)[0][0] == ',' and re.findall(f',?{id_user},?', participantes)[0][-1] != ',':
                participantes = participantes.replace(f',{id_user}', '')
            elif re.findall(f',?{id_user},?', participantes)[0][0] != ',' and re.findall(f',?{id_user},?', participantes)[0][-1] == ',':
                participantes = participantes.replace(f'{id_user},', '')
            
            query_2 = "UPDATE grupos SET ids_participante = %s where id = %s"
            dados = (f'{participantes}', f'{id_grupo}')
            self._executar_comando(query_2, dados, True)
        else:
            participantes = participantes.replace(f'{id_user}', '')
            query_2 = "UPDATE grupos SET ids_participante = %s where id = %s"
            dados = (f'{participantes}', f'{id_grupo}')
            self._executar_comando(query_2, dados, True)

if __name__ == '__main__':
    gp = Grupo()
    gp.excluir_participante(3, 31)
    #print(gp.get_integrantes(8))
    #print(gp.inserir_participante(3, 25))