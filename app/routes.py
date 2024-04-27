from app import app
from flask import render_template, redirect, request

import app.services.usuarioService as usuarioService;
import app.services.empresaService as empresaService;
import app.services.avaliacaoService as avaliacaoService;

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/signup", methods=["GET", "POST"])
def cadastrar():
    if request.method == "GET":
        return render_template("cadastro_usuario.html")
    
    elif request.method == "POST":
        # extrair dados do formulario
        if(usuarioService.adicionarUsuario(None)): #substituir None por usuario
            return redirect("/empresas")
        else:
            return "erro"
        

@app.route("/empresas", methods=["GET"])
def empresas():
    return render_template("lista_empresas.html", empresas=empresaService.listarEmpresas())


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