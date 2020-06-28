from flask import Flask, url_for, redirect, request, render_template
from usuario import Usuario
from grupo import Grupo
from tarefa import Tarefa
import json

app = Flask(__name__)
user = None
esta_logado = None

@app.route('/home/<cadastro>', methods=['POST', 'GET'])
def home(cadastro):
    global user
    global esta_logado
    if request.method == 'POST':
        if cadastro != None or cadastro != '':
            if cadastro == 'cadastro':
                user = Usuario()
                nome = request.form['nome']
                email = request.form['email']
                senha = request.form['senha']
                user.cadastrar_usuario(nome, email, senha)
                try:
                    dados_user = json.loads(user.fazer_login(email, senha))
                    esta_logado = user.get_logado()
                    return render_template('home.html', user=dados_user)
                except Exception:
                    pass
                

            elif cadastro == 'logado':
                user = Usuario()
                email = request.form['email']
                senha = request.form['senha']
                dados_user = None

                try:
                    dados_user = json.loads(user.fazer_login(email, senha))
                    esta_logado = user.get_logado()
                    return render_template('home.html', user=dados_user)
                except Exception:
                    return render_template('login.html', erro=True)
    elif request.method == 'GET':
        if cadastro == 'log' and esta_logado:
            return render_template('home.html')
    

@app.route('/login', methods=['GET'])
def login():
    if esta_logado:
        return redirect(url_for('home', cadastro='log'))
    else:
        return render_template('login.html', erro=False)

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar.html')

@app.route('/grupos', methods=['GET'])
def grupos():
    if esta_logado:
        grupo = Grupo()
        grupos = grupo.pesquisar_grupos(user.get_id())
        return render_template('grupos.html', grupos=grupos)
    else:
        return 'você não está logado'

@app.route('/adicionar_no_grupo', methods=['POST'])
def adicionar_no_grupo():
    if esta_logado:
        id_grupo = request.form['idGrupo']
        id_user = request.form['idUser']
        grupo = Grupo()
        msg = grupo.inserir_participante(id_grupo, id_user)
        return msg
    else:
        return 'você não está logado'

@app.route('/carrega_tela_criar', methods=['GET'])
def carrega_tela_criar():
    if esta_logado:
        return render_template('criar_grupo.html')
    else:
        return 'você não está logado'

@app.route('/criar_grupo', methods=['POST'])
def criar_grupo():
    if esta_logado:
        nome = request.form['nomeGp']
        descricao = request.form['descricaoGp']
        gp = Grupo()
        gp.criar_grupo(nome, descricao, user.get_id())
        return 'grupo criado'
    else:
        return 'você não está logado'

@app.route('/sair_do_grupo', methods=['PUT'])
def sair_do_grupo():
    if esta_logado:
        id_grupo = request.form['idGrupo']
        id_user = request.form['idUser']
        grupo = Grupo()
        grupo.excluir_participante(id_grupo, id_user)
        return 'você saiu'
    else:
        return 'você não está logado'

@app.route('/acoes_grupo/<id_grupo>', methods=['GET'])
def acoes_grupo(id_grupo):
    if esta_logado:
        gp = Grupo()
        responsaveis = gp.get_integrantes(id_grupo)
        return render_template('acoes_grupo.html', id_grupo=id_grupo, responsaveis=responsaveis, user=user.get_id())
    else:
        return 'vc não está logado'

@app.route('/grupos/<id_grupo>', methods=['GET'])
def infos_grupos(id_grupo):
    if esta_logado:
        grupo = Grupo()
        infos = grupo.pegar_informacoes(id_grupo)
        return render_template('infos_grupo.html', gp=infos)
    else:
        return 'você não está logado'

@app.route('/integrantes/<id_grupo>', methods=['GET'])
def integrantes(id_grupo):
    if esta_logado:
        grupo = Grupo()
        infos = grupo.get_integrantes(id_grupo)
        return f'{infos}'
    else:
        return 'você não está logado'

@app.route('/tarefas_gp/<id_grupo>', methods=['GET'])
def tarefas_gp(id_grupo):
    if esta_logado:
        grupo = Grupo()
        tarefas = grupo.get_tarefas(id_grupo)
        id_user = user.get_id()
        return render_template('tarefasGrupo.html', tarefas=tarefas, id_user=id_user)
    else:
        return 'você não está logado'

@app.route('/marcar_feita', methods=['PUT'])
def marcar_feita():
    if esta_logado:
        id_tarefa = request.form['idTarefa']
        tarefa = Tarefa()
        tarefa.marcar_como_feita(id_tarefa)
        return 'status atualizado'
    else:
        return 'você não está logado'


@app.route('/criar_tarefa', methods=['POST'])
def criar_tarefa():
    #if esta_logado:
    if esta_logado:
        id_responsavel = request.form['idResponsavel']
        id_grupo = request.form['idGrupo']
        nome_tarefa = request.form['nomeTarefa']
        desc = request.form['desc']
        data_entrega = request.form['dataEntrega']

        tarefa = Tarefa()
        tarefa.criar_tarefa(id_responsavel, id_grupo, nome_tarefa, desc, data_entrega)

        return 'Tarefa criada!'
    else:
        return 'você não está logado'

@app.route('/remover_tarefa', methods=['POST'])
def remover_tarefa():
    if esta_logado:
        id = request.form['id_tarefa']
        tarefa = Tarefa()
        tarefa.excluir_tarefa(id)

        return 'Tarefa removida!'
    else:
        return 'você não está logado'

@app.route('/editar_tarefa/<id_tarefa>', methods=['GET'])
def mostrar_edit_tarefa(id_tarefa):
    if esta_logado:
        return render_template('editar_tarefa.html', id=id_tarefa)
    else:
        return 'vc não está logado'

@app.route('/editar_tarefa', methods=['PUT'])
def editar_resultado_tarefa():
    if esta_logado:
        id = request.form['id']
        desc = request.form['desc']
        tarefa = Tarefa()
        tarefa.editar_resultado(id, desc)
        return 'Tarefa editada com sucesso!'
    else:
        return 'vc não está logado'

@app.route('/ver_tarefas', methods=['GET'])
def ver_tarefas():
    if esta_logado:
        tarefa = Tarefa()
        lista_tarefas = tarefa.listar_tarefas(user.get_id())
        return render_template('tarefas.html', tarefas=lista_tarefas)
    else:
        return 'vc não está logado'

@app.route('/perfil', methods=['GET'])
def perfil():
    if esta_logado:
        return render_template('perfil.html', 
            id=user.get_id(), 
            nome=user.get_nome(),
            email=user.get_email())
    else:
        return 'vc não está logado'

@app.route('/sair', methods=['GET'])
def sair():
    global esta_logado
    if user:
        user.deslogar()
        esta_logado = False
        return redirect(url_for('login'))
    else:
        return 'invalido'
        
if __name__ == '__main__':
    app.run(debug=True)

