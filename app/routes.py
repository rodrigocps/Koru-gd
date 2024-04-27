# Neste módulo serão adicionadas as rotas, que processam as requisicoes, retornam as views e chamam os services.

from app import app
from flask import render_template, redirect, request

from app.services import usuarioService, empresaService, avaliacaoService

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/signup", methods=["GET", "POST"])
def cadastrar():
    if request.method == "GET":
        return render_template("cadastro_usuario.html")
    
    elif request.method == "POST":
        usuario = {
            "nome" : request.form['nome'],
            "email" : request.form['email'],
            "senha" : request.form['senha']
        }

        success, msg = usuarioService.adicionarUsuario(usuario);

        if(success): #substituir None por usuario
            return redirect("/empresas")
        else:
            return render_template("cadastro_usuario.html", msg=msg)
        

@app.route("/empresas", methods=["GET"])
def empresas():
    pagina = request.args.get("pagina", default=1, type=int)

    empresas = empresaService.listarEmpresas(pagina);
    return render_template("lista_empresas.html", empresas=empresas, pagina=pagina)


@app.route("/empresa/<empresaId>", methods=["GET"])
def empresa(empresaId):
    return render_template("empresa.html", empresa=empresaService.getEmpresa(empresaId))


@app.route("/empresa/<empresaId>/adicionarAvaliacao", methods=["GET", "POST"])
def adicionar_avaliacao(empresaId):
    if request.method == "GET":
        return render_template("adicionar_avaliacao.html")
    
    elif request.method == "POST":
        # extrair dados do formulario
        if(avaliacaoService.adicionarAvaliacao(None, empresaId)): #substituir (None, empresaId) por (avaliacao, empresaId)
            return redirect("/empresa")
        else:
            return "erro"