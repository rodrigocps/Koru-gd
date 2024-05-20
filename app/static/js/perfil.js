document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/usuarios/profile")
        	.then(response => {
                if(!response.ok)
                    throw new Error("Erro ao buscar perfil de usuário.")
                return response.json()
            })
            .then(data => {
                renderPerfil(data)
            }).catch(error => console.log("Erro ao buscar perfil de usuário.", error))
})

function renderPerfil(data){
    const nome = document.getElementById("nome")
    const email = document.getElementById("email")

    nome.value = data.nome
    email.value = data.email

    const editNomeBtn = document.getElementById("edit-nome-btn")
    editNomeBtn.addEventListener("click", () => {
        nome.disabled = !nome.disabled
        if(!nome.disabled) {
            nome.focus()
            email.disabled = true
            editNomeBtn.textContent = "Salvar"
        } else {
            editNomeBtn.textContent = "Editar"
        }
    })

    const editEmailBtn = document.getElementById("edit-email-btn")
    editEmailBtn.addEventListener("click", () => {
        email.disabled = !email.disabled
        if(!email.disabled) {
            email.focus()
            nome.disabled = true
            editEmailBtn.textContent = "Salvar"
        } else {
            editEmailBtn.textContent = "Editar"
        }
    })

    const list = [nome, email]
    list.forEach(prop => {
        prop.addEventListener("change", () => {
            renderSaveButtons({nome:nome, email:email})
        })
    })

}

function renderSaveButtons(body) {
    const btnDiv = document.getElementById("btns-div")
    btnDiv.innerHTML = ""

    const save = document.createElement("button")
    save.classList.add("btn", "btn-primary")
    save.textContent = "Salvar alterações"

    const cancel = document.createElement("button")
    cancel.classList.add("btn", "btn-secondary")
    cancel.textContent = "Reverter alterações"

    save.addEventListener("click", () => {
        fetch("/usuarios/profile/edit", {
            headers : {
                "Content-type" : "application/json"
            },
            method: "PUT",
            body: JSON.stringify({
                nome : body.nome.value,
                email: body.email.value
            })
        }).then(response => {
            if(!response.ok) throw new Error("Erro ao atualizar usuario");
        }).catch(error => console.log("Erro ao atualizar de usuário.", error))
    })


    btnDiv.append(save)
    btnDiv.append(cancel)

}