# Neste módulo serão adicionadas as rotas, que processam as requisicoes, retornam as views e chamam os services.

from app import app
from flask import render_template, redirect, request, url_for

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

        if(success):
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
    pagina = request.args.get("fromPage", default=1, type=int)

    avaliacoes = avaliacaoService.getAvaliacoes(empresaId)
    empresa=empresaService.getEmpresa(empresaId)
    return render_template("empresa.html", empresa=empresa, avaliacoes=avaliacoes, pagina=pagina)


@app.route("/empresa/<empresaId>/avaliacoes/adicionar", methods=["GET", "POST"])
def adicionar_avaliacao(empresaId):
    if request.method == "GET":
        return render_template("adicionar_avaliacao.html", codigoEmpresa = empresaId)
    
    elif request.method == "POST":
        avaliacao = {
            "titulo" : request.form["titulo"],
            "texto" : request.form["texto"]
        }

        sucesso, msg = avaliacaoService.adicionarAvaliacao(avaliacao, empresaId)
        if sucesso:
            return redirect(url_for("empresa", empresaId=empresaId)) 
        else:
            return msg
        

@app.route("/empresa/<empresaId>/avaliacoes/excluir/<avaliacaoId>", methods=["GET" , "POST"])
def excluir_avaliacao(empresaId, avaliacaoId):
    avaliacaoService.excluirAvaliacao(empresaId, avaliacaoId)
    return redirect(url_for("empresa", empresaId=empresaId))

@app.route("/empresa/<empresaId>/avaliacoes/editar/<avaliacaoId>", methods=["GET" , "POST"])
def editar_avaliacao(empresaId, avaliacaoId):
    if(request.method == "GET"):
        avaliacao = avaliacaoService.getAvaliacao(empresaId, avaliacaoId)
        if(avaliacao):
            return render_template("adicionar_avaliacao.html", codigoEmpresa = empresaId, avaliacao=avaliacao)
        else:
            return "Avaliacao não encontrada."
    elif(request.method == "POST"):
        avaliacao = {
            "id" : avaliacaoId,
            "titulo" : request.form["titulo"],
            "texto" : request.form["texto"]
        }
        avaliacaoService.editarAvaliacao(empresaId, avaliacao)
    return redirect(url_for("empresa", empresaId=empresaId))