from app import app
from flask import render_template
import json

import app.services.usuarioServices as usuarioServices;

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/signup", methods=["GET"])
def cadastrar_page():
    if(usuarioServices.adicionarUsuario):
        return render_template("cadastro_usuario.html")
    else:
        return "erro"

@app.route("/signup", methods=["POST"])
def cadastro():
    return "Usuario cadastrado"

@app.route("/empresas", methods=["GET"])
def empresas():
    empresas = json.load(open("./1100_empresas.json", encoding="utf8"))
    empresas_ordenadas = sorted(empresas, key=lambda x: x['nome'])

    return render_template("lista_empresas.html", empresas=empresas_ordenadas)