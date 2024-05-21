function fetchEmpresas (pagina, search, byName, bySetor) {
    let fetchUrl = "/api/empresas"
    const params = new URLSearchParams()
    
    if(pagina) params.append("pagina",pagina)
    if(search) params.append("search", search)
    if(byName) params.append(byName, 1)
    if(bySetor) params.append(bySetor, 1)

    if(pagina||search)
        fetchUrl = fetchUrl + `?` + params.toString()

    fetch(fetchUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao buscar dados: ' + response.status);
            }
            
            return response.json()
        })
        .then(data =>{
            renderEmpresas(data, params)
        })
        .catch(error => console.log(error))
}

function renderEmpresas(data, params) {
    const {empresas, totalPaginas} = data;
    const listaDiv = document.querySelector("div.lista")
    listaDiv.innerHTML = ""

    if(empresas.length > 0) {
        const title = document.createElement("h2")
        title.textContent = "Empresas para você avaliar"
        
        const row = document.createElement("div")
        row.classList.add("empresas-row", "row", "row-cols-1", "row-cols-lg-2", "row-cols-xl-2")
    
        empresas.forEach(empresa => {
            const elem = getColElement(empresa)
            if(elem)
                row.appendChild(elem)
        });


        listaDiv.appendChild(title)

        listaDiv.appendChild(row)

        renderPagination(totalPaginas, params)
    }
    else {
        const emptyMessage = document.createElement("span")
        emptyMessage.className = "empty-message"

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

function renderPagination(maxPaginas, params, divAlternativa){
    if(maxPaginas == 1) return;

    const root = document.getElementById("root")

    const paginaAtual = params.get("pagina") ? Number(params.get("pagina"))  : 1

    const navExistente = divAlternativa ? divAlternativa : document.querySelector(".pagination-nav")
    if(navExistente) navExistente.innerHTML = ""

    const nav = navExistente ? navExistente : document.createElement("div");
    nav.classList.add("pagination", "pagination-nav")
    nav.ariaLabel = "..."


    const anteriorLi = document.createElement("li")
    anteriorLi.classList.add("page-item")

    const anterior = document.createElement("a")
    anterior.classList.add("page-link", "filled")
    anterior.textContent = "Página anterior"
    anterior.href = "/?" + defParam("pagina", (paginaAtual - 1)).toString()

    const proximaLi = document.createElement("li")
    proximaLi.classList.add("page-item")

    const proxima = document.createElement("a")
    proxima.classList.add("page-link", "filled")
    proxima.textContent = "Proxima página"
    proxima.href = "/?" + defParam("pagina", (paginaAtual + 1)).toString()

    const dotsLi = document.createElement("li")
    dotsLi.classList.add("page-item")

    const dots = document.createElement("a")
    dots.classList.add("page-link", "disabled")
    dots.textContent = "..."


    if(paginaAtual > 1) nav.appendChild(anterior)
    
    if(maxPaginas < 7 && maxPaginas > 0){
        adicionarPaginas(nav, 1, maxPaginas, paginaAtual)
        if(paginaAtual < maxPaginas) nav.appendChild(proxima)
        root.appendChild(nav)
        return;
    }

    let inicio = paginaAtual > 2 ? paginaAtual - 1 : 1
    let fim = paginaAtual > 2 ? paginaAtual + 1 : 3 

    if(paginaAtual >= maxPaginas - 6) {
        adicionarPaginas(nav, maxPaginas - 6, maxPaginas - 2, paginaAtual)
    }else{
        adicionarPaginas(nav, inicio, fim, paginaAtual)
        nav.appendChild(dots)
    }

    adicionarPaginas(nav, maxPaginas - 1, maxPaginas, paginaAtual)
    
    if(paginaAtual < maxPaginas) nav.appendChild(proxima)

    root.appendChild(nav)

}

function adicionarPaginas(nav, inicio, fim, paginaAtual, params) {

    for(let i=inicio; i<=fim; i ++) {
        const li = document.createElement("li")
        li.classList.add("page-item")

        const a = document.createElement("a")
        a.classList.add("page-link")
        a.textContent = i
        a.href = window.location.pathname + `?` + defParam("pagina", i).toString()

        if(i == paginaAtual) {
            a.classList.add("active")
        }

        nav.appendChild(a)
    }
}

function defParam(param, value){
    const params = new URLSearchParams(window.location.search);

    const parametroExistente = params.get(param);

    if (parametroExistente === null) {
        params.append(param, value);
    } else {
        params.set(param, value);
    }
    return params
    
}

document.addEventListener('DOMContentLoaded', function() {
        const params = new URLSearchParams(window.location.search);
        const pagina = params.get("pagina") ? params.get("pagina") : 1
        const search = params.get("search") ? params.get("search") : null
        const byName = params.get("SEARCH_BY_NAME") ? "SEARCH_BY_NAME" : null
        const bySetor = params.get("SEARCH_BY_SETOR") ? "SEARCH_BY_SETOR" : null
        fetchEmpresas(pagina, search, byName, bySetor);
    }
)

