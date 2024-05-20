document.addEventListener("DOMContentLoaded", () => {
    const profileContent = document.querySelector(".profile-content")
    profileContent.innerHTML = ""

    const navTabs = document.createElement("ul")
    navTabs.classList.add("nav", "nav-tabs")

    const tabContent = document.createElement("div")
    tabContent.classList.add("tab-content")

    appendTab("Minhas avaliações", `#minhas-avaliacoes`, navTabs,() => renderMinhasAvaliacoes(tabContent), true)
    appendTab("Outros usuários", `#outros-usuarios`, navTabs,() => renderOutrosUsuarios(tabContent), false)

    profileContent.append(navTabs)
    profileContent.append(tabContent)
})

const appendTab = (label, hash, navTabs, renderFn, isDefault) => {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.textContent = label;
    li.classList.add("nav-item");
    a.classList.add("nav-link");

    a.href = `${window.location.pathname}${hash}`
    console.log(window.location.hash.slice(1))

    if(window.location.hash==hash || (!window.location.hash && isDefault)){
        a.classList.add("active")
        a.click()
        renderFn()
    }

    a.addEventListener("click", () => {
        navTabs.querySelectorAll("a.nav-link").forEach(anchor => anchor.classList.remove("active"))
        a.classList.add("active")
        renderFn()
    })

    li.append(a)
    navTabs.append(li)
}

const renderMinhasAvaliacoes = (tabContent) => {
    tabContent.innerHTML = "Minhas avaliacoes"

}

const renderOutrosUsuarios = (tabContent) => {
    tabContent.innerHTML = ""
    const form = document.createElement("form")
    form.classList.add("search-user")

    const formGroup = document.createElement("div")
    formGroup.classList.add("form-group")

    const nameInput = document.createElement("input")
    nameInput.classList.add("form-control")
    nameInput.type = "text"
    nameInput.id = "nome"
    nameInput.name = "nome"

    const nameInputLabel = document.createElement("label")
    nameInputLabel.htmlFor = "nome"
    nameInputLabel.textContent = "Pesquise por um usuário:"

    formGroup.append(nameInputLabel)
    formGroup.append(nameInput)

    form.append(formGroup)

    addFormCheckbox("searchByName", "SEARCH_BY_NAME", "Pesquisar por Nome", form)
    addFormCheckbox("searchByEmail", "SEARCH_BY_EMAIL", "Pesquisar por Email", form)
    addFormCheckbox("searchById", "SEARCH_BY_ID", "Pesquisar por Id", form)

    const queryParams = new URLSearchParams(window.location.search)

    form.querySelectorAll(".form-check-input").forEach(checkbox => {
        checkbox.addEventListener("click", () => {
            if(checkbox.checked) {
                queryParams.delete(checkbox.name)
                queryParams.append(checkbox.name, 1)
            }else{
                queryParams.delete(checkbox.name)
            }
            console.log(queryParams.toString())
        })
    })

    const submitBtn = document.createElement("button")
    submitBtn.classList.add("btn", "btn-primary")
    submitBtn.id = "searchUserBtn"
    submitBtn.type = "submit"
    submitBtn.textContent = "Pesquisar"

    submitBtn.addEventListener("click", (event) => {
        event.preventDefault()
        if(nameInput !== "") {
            queryParams.append("nome", nameInput.value)
        }
        const paramSize = Array.from(queryParams.keys()).length;
        window.location.href = window.location.pathname +  window.location.hash +`${paramSize > 0 ? "?" + queryParams : ""}`
    })

    form.append(submitBtn)

    tabContent.append(form)
}

const addFormCheckbox = (id, name, label, form) => {
    const formCheck = document.createElement("div")
    formCheck.classList.add("form-check")

    const input = document.createElement("input")
    input.classList.add("form-check-input")
    input.type = "checkbox"
    input.name = name
    input.id = id

    const inputLabel = document.createElement("label")
    inputLabel.classList.add("form-check-label")
    inputLabel.htmlFor = id
    inputLabel.textContent = label

    formCheck.append(input)
    formCheck.append(inputLabel)
    
    form.append(formCheck)
}
