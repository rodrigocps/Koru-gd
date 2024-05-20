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
    defaultValues = data

    const changeDefaultValuesFn = (newValues) => {
        defaultValues = newValues
    }

    const nome = document.getElementById("nome")
    const email = document.getElementById("email")

    nome.value = defaultValues.nome
    email.value = defaultValues.email

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
        if(nome.value.trim() !== defaultValues.nome.trim()){
            renderSaveButtons({nome:nome, email:email}, defaultValues, changeDefaultValuesFn)
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
        
        if(email.value.trim() !== defaultValues.email.trim()){
            renderSaveButtons({nome:nome, email:email}, defaultValues, changeDefaultValuesFn)
        }
    })

}


function renderSaveButtons(body, data, changeDefaultValuesFn) {
    const btnDiv = document.getElementById("btns-div")
    btnDiv.innerHTML = ""

    const save = document.createElement("button")
    save.classList.add("btn", "btn-primary")
    save.textContent = "Salvar alterações"


    save.addEventListener("click", () => {
        fetch("/api/usuarios/" + data.id, {
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
            return response.json()
        }).then((data) => {
            btnDiv.innerHTML = ""
            changeDefaultValuesFn({...defaultValues, ...data})
        })
        .catch(error => console.log("Erro ao atualizar de usuário.", error))
    })


    btnDiv.append(save)
    if(body.nome.value !== data.nome || body.email.value !== data.email){ 
        const cancel = document.createElement("button")
        cancel.classList.add("btn", "btn-secondary")
        cancel.textContent = "Reverter alterações"
        cancel.addEventListener("click", () => {
            body.nome.value = data.nome
            body.email.value = data.email
            btnDiv.innerHTML = ""
        })
        
        btnDiv.append(cancel)
    }
        

}
