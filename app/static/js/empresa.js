const params = new URLSearchParams(window.location.search);

const id = params.get('id');

if(id) {
    fetch("/api/empresas/" + id)
        .then(response => {
            if(response.ok)
                return response.json()
            else {
                throw new Error('Erro ao buscar dados: ' + response.status);
            }
        }).then(data => {
            const nome = document.getElementById("nome-empresa")
            const setor = document.getElementById("setor-empresa")

            nome.textContent = data.nome
            setor.textContent = data.setor
        }).catch(error => console.log(error))

        
}

document.addEventListener('DOMContentLoaded', function() {
    renderAvaliacoes();
});

function renderAvaliacoes() {
    const params = new URLSearchParams(window.location.search);
    const empresaId = params.get('id');

    const list = document.getElementById("avaliacoes-list")
    list.innerHTML = ""

    fetch(`/api/empresas/${empresaId}/avaliacoes`)
        .then(response => {
            if(response.ok)
                return response.json()
            else {
                throw new Error('Erro ao buscar dados: ' + response.status);
            }
        }).then(data => {
            if(data.length > 0) {
                data.sort(compararPorId).forEach(avaliacao => {
                    if(avaliacao.titulo && avaliacao.texto) {
                        const li = document.createElement("li");
                        li.className = "avaliacao-li"
    
                        const title = document.createElement("h3")
                        title.textContent = avaliacao.titulo
    
                        const text = document.createElement("p")
                        text.textContent = avaliacao.texto

                        const authorName = document.createElement("span")
                        authorName.className = "avaliacao-author-name"
                        authorName.textContent = "Author: " + avaliacao.autor_name
    
                        li.appendChild(title)
                        li.appendChild(text)
                        li.appendChild(authorName)

                        if(avaliacao.isClientOwner) 
                            renderButtonsDiv(li)

                        list.appendChild(li)
                    }
                });
            }
        }).catch(error => console.log(error))
}

function renderAddAvaliacao(){
    const avaliacoesDiv = document.getElementById("avaliacoes-div")
        if(avaliacoesDiv) {
            const user = localStorage.getItem("user")
            if(user){
                const form = `
                    <div class="avaliacoes-div>"
                        <h3>Adicione uma avaliação</h3>
                        <label for="titulo">Digite o título: </label>
                        <input 
                            id="titulo" 
                            name="titulo"
                            type="text" 
                            required
                        />
                        
                        <label for="texto">Digite o texto: </label>
                        <textarea 
                            id="texto" 
                            name="texto" 
                            required
                        >{{texto}}</textarea>
                        
                        <button type="button" onclick="addAvaliacao()">Enviar</button>
                    </div>
                `
                const avaliacoesForm = document.createElement("div")
                avaliacoesForm.className = "avaliacoes-form"
                avaliacoesForm.innerHTML = form
            }
            else {
                avaliacoesDiv.innerHTML = `
                    <div class="login-avaliacoes-div">
                        <p class="add-avaliacao-text">Faça login para adicionar uma avaliação</p>
                        <a href="/login" class="login-button">Entrar</a>
                    </div>
                `
            }

        }
    
}

function addAvaliacao() {
    const params = new URLSearchParams(window.location.search);
    const empresaId = params.get('id');
    
    const titulo = document.querySelector("#avaliacao-form > #titulo")
    const texto = document.querySelector("#avaliacao-form > #texto")
    const avaliacao = {
        titulo : titulo.value,
        texto : texto.value
    }
    fetch(`/api/empresas/${empresaId}/avaliacoes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(avaliacao),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao enviar o formulário');
            } 
            
            titulo.value = ""
            texto.value = ""
            renderAvaliacoes()
        })
        .catch(error => {
            console.error('Erro:', error);
        });
}

function editarAvaliacao(li, empresaId, avaliacaoId, titulo, texto) {
    li.innerHTML = ""
    
    const tituloLabel = document.createElement("span")
    tituloLabel.textContent = "Digite um titulo: "

    const tituloInput = document.createElement("input")
    tituloInput.className = "edit-titulo-input"
    tituloInput.value = titulo

    const textLabel = document.createElement("span")
    textLabel.textContent = "Digite um texto: "

    const textInput = document.createElement("textarea")
    textInput.className = "edit-text-input"
    textInput.value = texto

    const editTileButtons = document.createElement("div")
    editTileButtons.className = "edit-tile-buttons"

    const saveButton = document.createElement("button")
    saveButton.type = "button"
    saveButton.textContent = "Salvar"
    saveButton.addEventListener("click", () => {
        const avaliacao = {
            titulo : tituloInput.value,
            texto : textInput.value
        }
        if((titulo!==avaliacao.titulo) || (texto!==avaliacao.texto)) {
            fetch(`/api/empresas/${empresaId}/avaliacoes/${avaliacaoId}`, {
                method: 'PUT',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify(avaliacao),
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Erro ao enviar o formulário');
                    } 
                    
                    titulo.value = ""
                    texto.value = ""
                    renderAvaliacoes()
                })
                .catch(error => {
                    console.error('Erro:', error);
                });
        }
    } )

    const cancelButton = document.createElement("button")
    cancelButton.type = "button"
    cancelButton.textContent = "Cancelar"

    editTileButtons.appendChild(saveButton)
    editTileButtons.appendChild(cancelButton)

    li.appendChild(tituloLabel)
    li.appendChild(tituloInput)
    li.appendChild(textLabel)
    li.appendChild(textInput)
    li.appendChild(editTileButtons)
}

function deletarAvaliacao(empresaId, avaliacaoId) {
    fetch(`/api/empresas/${empresaId}/avaliacoes/${avaliacaoId}`, {
        method: 'DELETE'
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao enviar o formulário');
            } 
            else renderAvaliacoes()
        })
        .catch(error => {
            console.error('Erro:', error);
        });
}

function compararPorId(a, b) {
    return b.id - a.id;
}

function renderButtonsDiv(li) {
    user = localStorage.getItem("user")
    if(user) {
        const buttonsdiv = document.createElement("div")
        buttonsdiv.className = "avaliacao-buttons-div"

        const editButton = document.createElement("button")
        editButton.className = "edit-button"
        editButton.type = "button"
        editButton.textContent = "Editar"
        editButton.addEventListener("click", () => editarAvaliacao(li, empresaId, avaliacao.id, avaliacao.titulo, avaliacao.texto))

        const deleteButton = document.createElement("button")
        deleteButton.className = "delete-button"
        deleteButton.type = "button"
        deleteButton.textContent = "Excluir"
        deleteButton.addEventListener("click", () => deletarAvaliacao(empresaId, avaliacao.id))
    
        buttonsdiv.appendChild(editButton)
        buttonsdiv.appendChild(deleteButton)
    
        li.appendChild(buttonsdiv)
    }
}