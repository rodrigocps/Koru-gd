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

    const params = getPageSearchParams()
    a.href = `${window.location.pathname}${hash}`

    if(formatHash(window.location.hash)==hash || (!window.location.hash && isDefault)){
        a.href += `${params ? params : ""}`
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

    const searchInput = document.createElement("input")
    searchInput.classList.add("form-control", "search-input")
    searchInput.type = "text"
    searchInput.id = "search"
    searchInput.name = "search"

    const searchInputLabel = document.createElement("label")
    searchInputLabel.htmlFor = "search"
    searchInputLabel.textContent = "Pesquise por um usuário:"

    formGroup.append(searchInputLabel)
    formGroup.append(searchInput)

    form.append(formGroup)

    const params = new URLSearchParams(getPageSearchParams())
    const sizeParams = Array.from(params.keys()).length;

    let checkboxList = [
        addFormCheckbox("searchByName", "SEARCH_BY_NAME", "Pesquisar por Nome", (sizeParams > 0) ? params.has("SEARCH_BY_NAME") : true, form),
        addFormCheckbox("searchByEmail", "SEARCH_BY_EMAIL", "Pesquisar por Email", (sizeParams > 0) ? params.has("SEARCH_BY_EMAIL") : true, form),
        addFormCheckbox("searchById", "SEARCH_BY_ID", "Pesquisar por Id", (sizeParams > 0) ? params.has("SEARCH_BY_ID") : true, form)
    ]


    const submitBtn = document.createElement("button")
    submitBtn.classList.add("btn", "btn-success")
    submitBtn.id = "searchUserBtn"
    submitBtn.type = "submit"
    submitBtn.textContent = "Pesquisar"

    submitBtn.addEventListener("click", (event) => {
        event.preventDefault()

        const queryParams = new URLSearchParams(getPageSearchParams())
        checkboxList.forEach(checkbox => {
            if(checkbox.checked) {
                queryParams.set(checkbox.name, 1)
            }
        })

        if(searchInput.value !== "") {
            queryParams.set("search", searchInput.value)
        } else queryParams.delete("search")
        const paramSize = Array.from(queryParams.keys()).length;
        window.location.href = window.location.pathname +  formatHash(window.location.hash) +`${paramSize > 0 ? "?" + queryParams : ""}`

        renderUsersList(queryParams, tabContent)
    })

    form.append(submitBtn)

    tabContent.append(form)
}

const renderUsersList = (queryParams, tabContent) => {
    const paramSize = Array.from(queryParams.keys()).length;
    fetch("api/usuarios" + `${paramSize > 0 ? "?" + queryParams : ""}`)
        .then(response => {
            if(!response.ok) throw new Error("Erro ao buscar usuarios..")
            return response.json()
        }).then((data) => {
        const avList = document.getElementById("avaliacoes-list")
        if(avList) avList.remove()
        const tableDivExist = document.querySelector(".table-div")

        let tableDiv;
        if(tableDivExist) {
            tableDivExist.innerHTML = ""
            tableDiv = tableDivExist
        } else {
            tableDiv = document.createElement("div")
            tableDiv.classList.add("table-div")
        }

        if(data.length > 0) {
            let table = document.createElement("table")
            table.classList.add("users-table", "table", "table-striped")

            const head = document.createElement("thead")
            const headRow = document.createElement("tr")

            addHeadColumns(headRow, "Id", "Nome", "Email", "Ações")

            head.append(headRow)
            table.append(head)

            const body = document.createElement("tbody")
            data.forEach(user => {
                const row = document.createElement("tr")
                addTableRowColumn(user.id, row, "row")
                addTableRowColumn(user.nome, row)
                addTableRowColumn(user.email, row)
                addButtonToRow("Ver Avaliacoes", row, () => {
                    renderUserAvaliacoesList(user, tabContent, table, tableDiv)
                })
                
                body.append(row)
            })
            table.append(body)

            tableDiv.append(table)
            tabContent.append(tableDiv)
        }
        else {
            const noResultsDiv = document.createElement("div")
            noResultsDiv.classList.add("no-results-msg")

            noResultsDiv.textContent = "Nenhum resultado encontrado."

            tableDiv.append(noResultsDiv)
        }
}).catch((error) => console.log(error))
}

const renderUserAvaliacoesList = (user, tabContent, table, tableDiv) => {
    const from = table;
    table.remove()
    const avaliacoesDiv = document.createElement("div")
    avaliacoesDiv.id = "avaliacoes-list"

    tabContent.append(avaliacoesDiv)

    renderAllAvaliacoes(user.id)

    const backButton = document.createElement("button")
    backButton.classList.add("btn", "btn-outline-success")
    backButton.textContent = "Voltar à tabela"
    backButton.addEventListener("click", () => {
        tableDiv.append(from)
        avaliacoesDiv.remove()
    })

    avaliacoesDiv.append(backButton)

}

const addHeadColumns = (headRow, ...args) => {
    args.forEach(label => {
        const column = document.createElement("th")
        column.scope = "col"
        column.textContent = label
        headRow.append(column)
    })
}

const addTableRowColumn = (text, row, scope) => {
    const col = document.createElement("td")
    if(scope) col.scope = scope
    col.textContent = text

    row.append(col)
}

const addButtonToRow = (text, row, onClick) => {
    const col = document.createElement("td")

    const button = document.createElement("button")
    button.classList.add("btn", "btn-outline-success")
    button.type = button
    button.textContent = text
    button.addEventListener("click", () => onClick())

    col.append(button)

    row.append(col)
}

const addFormCheckbox = (id, name, label, state, form) => {
    const formCheck = document.createElement("div")
    formCheck.classList.add("form-check")

    const input = document.createElement("input")
    input.classList.add("form-check-input")
    input.type = "checkbox"
    input.name = name
    input.id = id
    input.checked = state

    const inputLabel = document.createElement("label")
    inputLabel.classList.add("form-check-label")
    inputLabel.htmlFor = id
    inputLabel.textContent = label

    formCheck.append(input)
    formCheck.append(inputLabel)
    
    form.append(formCheck)

    return input
}

const formatHash = (hash) => {
    let returnValue = ""
    for(let i=0; i < hash.length; i++){
        if(hash[i] === "&" || hash[i] === "?"){
            return returnValue;
        }
        else returnValue += hash[i]
    }
    return returnValue
}

const getPageSearchParams = () => {
    const href = window.location.href.toString()
    let returnValue = ""

    let start = false
    for(let i=0; i < href.length; i++){
        if(href[i] == "?") start = true
        else if(href[i] == "#" && returnValue.length > 0) return returnValue;

        if(start){
            returnValue += href[i]
        }
    }
    return returnValue
}
