from conexao import Conexao
from datetime import date

class Tarefa(object):
    def __init__(self):
        self._dados_conexao = {'user': 'root', 'password': '', 
            'host': '127.0.0.1', 'database': 'app_tarefas_estacio'}
        self._conexao = Conexao(self._dados_conexao).conexao
        self._cursor = self._conexao.cursor()

    def _executar_comando(self, query="", dados="", salvar=False):
        self._cursor.execute(query, dados)
        if salvar:
            self._conexao.commit()
        

    def criar_tarefa(self, id_responsavel, id_grupo, nome_tarefa, descricao, data_entrega):
        query = "INSERT INTO tarefas(id_responsavel, id_grupo, nome_tarefa, descricao, data_entrega)VALUES(%s, %s, %s, %s, %s)"
        dados = (f'{id_responsavel}', f'{id_grupo}', f'{nome_tarefa}', f'{descricao}', f'{data_entrega}')
        self._executar_comando(query, dados, True)

    def listar_tarefas(self, id):
        query = f'select t.* from tarefas t where t.id_responsavel = {id}'
        lista = []
        self._executar_comando(query)
        for (id, id_responsavel, id_grupo, nome_tarefa, descricao, data_inicio, data_entrega, dta_feita, resultado) in self._cursor:
            dic = {"id": id, "id_responsavel": id_responsavel, "id_grupo": id_grupo, "nome_tarefa": nome_tarefa, "descricao": descricao, "data_inicio": data_inicio, "data_entrega": data_entrega, "dta_feita": dta_feita, "resultado": resultado}
            lista.append(dic)
        return lista

    def excluir_tarefa(self, id):
        query = f"delete from tarefas where id={id}"
        self._executar_comando(query, salvar=True)

    def marcar_como_feita(self, id, data_feita):
        query = "UPDATE tarefas t SET t.dta_feita = %s where t.id = %s"
        dados = (f'{data_feita}', f'{id}')
        self._executar_comando(query, dados, True)
    
    def buscar_nao_nulas(self, id_responsavel):
        query = f'select t.* from tarefas t where t.id_responsavel = {id_responsavel} and t.dta_feita is not null'
        lista = []
        self._executar_comando(query)
        for (id, id_responsavel, id_grupo, nome_tarefa, descricao, data_inicio, data_entrega, dta_feita, resultado) in self._cursor:
            dic = {"id": id, "id_responsavel": id_responsavel, "nome_tarefa": nome_tarefa, "descricao": descricao, "data_inicio": data_inicio, "data_entrega": data_entrega, "dta_feita": dta_feita}
            lista.append(dic)
        return lista

    def buscar_nulas(self, id_responsavel):
        query = f'select t.* from tarefas t where t.id_responsavel = {id_responsavel} and t.dta_feita is null'
        lista = []
        self._executar_comando(query)
        for (id, id_responsavel, id_grupo, nome_tarefa, descricao, data_inicio, data_entrega, dta_feita, resultado) in self._cursor:
            dic = {"id": id, "id_responsavel": id_responsavel, "nome_tarefa": nome_tarefa, "descricao": descricao, "data_inicio": data_inicio, "data_entrega": data_entrega, "dta_feita": dta_feita}
            lista.append(dic)
        return lista
        
if __name__ == "__main__":
    tarefa = Tarefa()
    tarefa.criar_tarefa(24, 1, 'apresentar trabalho', 'apresentar um app feito para gerenciamento de tarefas', '2020/06/23')
    #tarefa.excluir_tarefa(8)
    #print(tarefa.buscar_nao_nulas(24))
    #tarefa.marcar_como_feita(6, date.today())