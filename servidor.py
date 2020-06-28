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

@app.route('/acoes_grupo/<id_grupo>', methods=['GET'])
def acoes_grupo(id_grupo):
    if esta_logado:
        return render_template('acoes_grupo.html', id=id_grupo)
    else:
        return 'vc não está logado'

@app.route('/grupos/<id_grupo>', methods=['GET'])
def infos_grupos(id_grupo):
    if esta_logado:
        grupo = Grupo()
        infos = grupo.pegar_informacoes(id_grupo)
        return render_template('infos_grupo.html', gp=infos)

@app.route('/integrantes/<id_grupo>', methods=['GET'])
def integrantes(id_grupo):
    grupo = Grupo()
    infos = grupo.get_integrantes(id_grupo)
    return f'{infos}'

@app.route('/tarefas_gp/<id_grupo>', methods=['GET'])
def tarefas_gp(id_grupo):
    if esta_logado:
        grupo = Grupo()
        tarefas = grupo.get_tarefas(id_grupo)
        id_user = user.get_id()
        return render_template('tarefasGrupo.html', tarefas=tarefas, id_user=id_user)

@app.route('/remover_tarefa', methods=['POST'])
def remover_tarefa():
    if esta_logado:
        id = request.form['id_tarefa']
        tarefa = Tarefa()
        tarefa.excluir_tarefa(id)

        return 'Tarefa removida!'

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

