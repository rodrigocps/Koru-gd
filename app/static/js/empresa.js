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
    renderAddAvaliacao()
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
                    if(avaliacao.titulo && avaliacao.texto && avaliacao.texto) {
                        const li = document.createElement("li");
                        li.className = "avaliacao-li"
                        renderAvaliacao(li, avaliacao)
                        list.appendChild(li)
                    }
                });
            }
        }).catch(error => console.log(error))
}

function renderAvaliacao(li, avaliacao){
    const title = document.createElement("h3")
    title.className = "avaliacao-titulo"
    title.textContent = avaliacao.titulo

    const text = document.createElement("p")
    text.className = "avaliacao-texto"
    text.textContent = avaliacao.texto

    const authorName = document.createElement("span")
    authorName.className = "avaliacao-author-name"
    authorName.textContent = "Author: " + avaliacao.autor_name

    li.appendChild(title)
    li.appendChild(text)
    li.appendChild(authorName)

    if(avaliacao.isClientOwner) 
        renderButtonsDiv(li, avaliacao)

}

function renderAddAvaliacao() {
    const avaliacaoDiv = document.getElementById("avaliacao-div");
    if (avaliacaoDiv) {
        const user = JSON.parse(localStorage.getItem("user"));
        if (user) {
            console.log(user);
            const form = `
                <div class="avaliacoes-div">
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
                    ></textarea>
                    
                    <button type="button" onclick="addAvaliacao()">Enviar</button>
                </div>
            `;
            const avaliacoesForm = document.createElement("div");
            avaliacoesForm.className = "avaliacoes-form";
            avaliacoesForm.innerHTML = form;
            avaliacaoDiv.appendChild(avaliacoesForm);
        } else {
            avaliacaoDiv.innerHTML = `
                <div class="login-avaliacoes-div">
                    <p class="add-avaliacao-text">Faça login para adicionar uma avaliação</p>
                    <a href="/login" class="login-button">Entrar</a>
                </div>
            `;
        }
    }
}

function addAvaliacao() {
    const params = new URLSearchParams(window.location.search);
    const empresaId = params.get('id');
    
    const titulo = document.querySelector(".avaliacoes-div > #titulo")
    const texto = document.querySelector(".avaliacoes-div > #texto")
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

function getEdicaoBlock(li,savedAvaliacao) {
    const edicaoBlock = document.createElement("div")
    edicaoBlock.className = "editar-avaliacao-block"

    const tituloLabel = document.createElement("span")
    tituloLabel.className = "edit-block-titulo-label"
    tituloLabel.textContent = "Digite um titulo: "

    const tituloInput = document.createElement("input")
    tituloInput.className = "edit-titulo-input"
    tituloInput.value = savedAvaliacao.titulo

    const textLabel = document.createElement("span")
    tituloLabel.className = "edit-block-text-label"
    textLabel.textContent = "Digite um texto: "

    const textInput = document.createElement("textarea")
    textInput.className = "edit-text-input"
    textInput.value = savedAvaliacao.texto

    edicaoBlock.appendChild(tituloLabel)
    edicaoBlock.appendChild(tituloInput)
    edicaoBlock.appendChild(textLabel)
    edicaoBlock.appendChild(textInput)
    edicaoBlock.appendChild(renderEditarAvaliacaoButtons(li,savedAvaliacao, tituloInput, textInput))

    return edicaoBlock
}

function renderEditarAvaliacaoButtons(li,savedAvaliacao, tituloInput, textInput) {
    const editTileButtons = document.createElement("div")
    editTileButtons.className = "edit-tile-buttons"

    const saveButton = document.createElement("button")
    saveButton.className = "update-avaliacao-submit-button"
    saveButton.type = "button"
    saveButton.textContent = "Salvar"
    saveButton.addEventListener("click", () => {
        const avaliacao = {
            titulo : tituloInput.value,
            texto : textInput.value
        }

        if((avaliacao.titulo!==savedAvaliacao.titulo) || (avaliacao.texto!==savedAvaliacao.texto)) {
            fetch(`/api/empresas/${savedAvaliacao.empresa_id}/avaliacoes/${savedAvaliacao.id}`, {
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
                    
                    renderAvaliacoes()
                })
                .catch(error => {
                    console.error('Erro:', error);
                });
        }
    } )

    const cancelButton = document.createElement("button")
    cancelButton.className = "update-avaliacao-cancel-button"
    cancelButton.type = "button"
    cancelButton.textContent = "Cancelar"
    cancelButton.addEventListener("click", () => {
        li.innerHTML = ""
        renderAvaliacao(li, savedAvaliacao)
    })

    editTileButtons.appendChild(saveButton)
    editTileButtons.appendChild(cancelButton)

    return editTileButtons
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

function renderButtonsDiv(li, avaliacao) {
    user = localStorage.getItem("user")
    if(user) {
        const buttonsdiv = document.createElement("div")
        buttonsdiv.className = "avaliacao-buttons-div"

        const editButton = document.createElement("button")
        editButton.className = "edit-button"
        editButton.type = "button"
        editButton.textContent = "Editar"
        editButton.addEventListener("click", () => editarAvaliacao(li, avaliacao))

        const deleteButton = document.createElement("button")
        deleteButton.className = "delete-button"
        deleteButton.type = "button"
        deleteButton.textContent = "Excluir"
        deleteButton.addEventListener("click", () => deletarAvaliacao(avaliacao.empresa_id, avaliacao.id))
    
        buttonsdiv.appendChild(editButton)
        buttonsdiv.appendChild(deleteButton)
    
        li.appendChild(buttonsdiv)
    }
}

function editarAvaliacao(li, avaliacao) {
    li.innerHTML = ""
    li.appendChild(getEdicaoBlock(li, avaliacao))
}