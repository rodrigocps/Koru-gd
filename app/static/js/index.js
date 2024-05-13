function fetchEmpresas (pagina, search) {
    const params = new URLSearchParams();
    if(pagina)
        params.append("pagina", pagina)

    if(search)
        params.append("search", search)

    let fetchUrl = "/api/empresas"

    if(pagina||search)
        fetchUrl = fetchUrl + "?" + params.toString()

    fetch(fetchUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao buscar dados: ' + response.status);
            }
            
            return response.json()
        })
        .then(data => renderEmpresas(data))
        .catch(error => console.log(error))
}

function renderEmpresas(data) {
    const listaDiv = document.querySelector("div.lista")
    listaDiv.innerHTML = ""

    if(data.length > 0) {

        const title = document.createElement("h2")
        title.textContent = "Empresas para você avaliar"
        
        const row = document.createElement("div")
        row.classList.add("empresas-row", "row", "row-cols-1", "row-cols-lg-2", "row-cols-xl-2")
    
        data.forEach(empresa => {
            const elem = getColElement(empresa)
            if(elem)
                row.appendChild(elem)
        });

        listaDiv.appendChild(title)
        listaDiv.appendChild(row)
        listaDiv.appendChild(pagination())
    }
    else {
        const emptyMessage = document.createElement("span")
        emptyMessage.className("empty-message")

        emptyMessage.textContent = "Não há empresas para mostrar" 

        listaDiv.appendChild(emptyMessage)
    }
}



function getColElement(empresa) {
    if (empresa.nome && empresa.id) {
        const col = document.createElement("div");
        col.classList.add("empresa-col", "col")

        const a = document.createElement("a")
        a.className = "empresa-element"
        a.href = "/empresas?id=" + empresa.id

        const empresaLogo = document.createElement("img")
        empresaLogo.classList.add("empresa-logo")
        empresaLogo.alt = "Logo da empresa"
        if(empresa.logo_url) empresaLogo.src = empresa.logo_url

        const nomeContainer = document.createElement("div")
        nomeContainer.className = "empresa-nome-container"


        const empresaName = document.createElement("span")
        empresaName.className = "empresa-name"
        empresaName.textContent =  empresa.nome;

        const empresaSetor = document.createElement("span")
        empresaSetor.className = "empresa-setor"
        empresaSetor.textContent =  empresa.setor;

        
        nomeContainer.appendChild(empresaName)
        nomeContainer.appendChild(empresaSetor)
        a.appendChild(empresaLogo)
        a.appendChild(nomeContainer)
        col.appendChild(a)

    
        return col;
    }
    return undefined
}

function search() {
    const search = document.getElementById("search").value

    if(search.length > 0 && !(/^[\s\t]*$/.test(search)) ) 
        fetchEmpresas(1, search)
    else {
        window.location.href = window.location.href
    }

}

function pagination(){
    const params = new URLSearchParams(window.location.search)

    const paginaAtual = params.get("pagina") ? Number(params.get("pagina")) : 1
    const search = params.get("search") ? params.get("search") : null
    const maxPaginas = 55

    const nav = document.createElement("nav");
    nav.classList.add("pagination", "pagination-nav")
    nav.ariaLabel = "..."

    const anteriorLi = document.createElement("li")
    anteriorLi.classList.add("page-item")

    const anterior = document.createElement("a")
    anterior.classList.add("page-link")
    anterior.textContent = "Anterior"
    anterior.href = "/?pagina=" + (paginaAtual - 1)

    const proximaLi = document.createElement("li")
    proximaLi.classList.add("page-item")

    const proxima = document.createElement("a")
    proxima.classList.add("page-link")
    proxima.textContent = "Proxima"
    proxima.href = "/?pagina=" + (paginaAtual + 1)

    const dotsLi = document.createElement("li")
    dotsLi.classList.add("page-item")

    const dots = document.createElement("a")
    dots.classList.add("page-link", "disabled")
    dots.textContent = "..."

    nav.appendChild(anterior)

    let inicio = paginaAtual > 3 ? paginaAtual - 2 : 1
    let fim = paginaAtual > 3 ? paginaAtual + 2 : 5 
    if(paginaAtual >= 49) {
        inicio = 49
        fim = 53
        adicionarPaginas(nav, inicio, fim, paginaAtual)
    }else{
        adicionarPaginas(nav, inicio, fim, paginaAtual)
        nav.appendChild(dots)
    }

    adicionarPaginas(nav, maxPaginas - 1, maxPaginas, paginaAtual)
    nav.appendChild(proxima)

    return nav

}

function adicionarPaginas(nav, inicio, fim, paginaAtual) {

    for(let i=inicio; i<=fim; i ++) {
        const li = document.createElement("li")
        li.classList.add("page-item")

        const a = document.createElement("a")
        a.classList.add("page-link")
        a.textContent = i
        a.href = window.location.pathname + `?pagina=${i}`

        if(i == paginaAtual) {
            a.classList.add("active")
        }
        // + `${search && ("&search=" + search)}`

        nav.appendChild(a)
    }

    // 1, 2, 3, 4, ..., 55

}

const params = new URLSearchParams(window.location.search)

const paginaAtual = params.get("pagina") ? params.get("pagina") : 1

fetchEmpresas(paginaAtual, null);