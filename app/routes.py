from app import app
from flask import render_template, redirect
import json

import app.services.usuarioService as usuarioService;
import app.services.empresaService as empresaService;
import app.services.avaliacaoService as avaliacaoService;

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/signup", methods=["GET"])
def cadastrar_page():
    return render_template("cadastro_usuario.html")

@app.route("/signup", methods=["POST"])
def cadastro():
    if(usuarioService.adicionarUsuario()):
        return redirect("/empresas")
    else:
        return "erro"

@app.route("/empresas", methods=["GET"])
def empresas():
    return render_template(empresas=empresaService.listarEmpresas())