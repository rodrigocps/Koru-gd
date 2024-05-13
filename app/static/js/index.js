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
    if(data.length > 0) {
        const listaDiv = document.querySelector("div.lista")
        listaDiv.innerHTML = ""

        const row = document.createElement("div")
        row.classList.add("empresas-row", "row", "row-cols-1", "row-cols-lg-2", "row-cols-xl-2")
    
        data.forEach(empresa => {
            const elem = getColElement(empresa)
            if(elem)
                row.appendChild(elem)
        });

        listaDiv.appendChild(row)
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

    if(search.length > 0) 
        fetchEmpresas(1, search)

}



fetchEmpresas(1, null);