function fetchEmpresas (pagina, search) {
    const params = new URLSearchParams();
    if(pagina)
        params.append("pagina", pagina)

    if(search)
        params.append("search", search)

    let fetchUrl = "/empresas"

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
        const listaDiv = document.querySelector("ul.lista-empresas")
        listaDiv.innerHTML = ""
    
        data.forEach(empresa => {
            const elem = getListElement(empresa)
            if(elem)
                listaDiv.appendChild(elem)
        });
    }
}

function getListElement(empresa) {
    if (empresa.nome && empresa.id) {
        const li = document.createElement("li");
        li.className = "empresa-li"

        const a = document.createElement("a")
        a.className = "empresa-element"
        a.href = "/empresas?id=" + empresa.id

        const empresaName = document.createElement("span")
        empresaName.className = "empresa-name"
        empresaName.textContent =  empresa.nome;

        const empresaSetor = document.createElement("span")
        empresaSetor.className = "empresa-setor"
        empresaSetor.textContent =  empresa.setor;

        a.appendChild(empresaName)
        a.appendChild(empresaSetor)
        li.appendChild(a)

    
        return li;
    }
    return undefined
}

function search() {
    const search = document.getElementById("search").value

    if(search.length > 0) 
        fetchEmpresas(1, search)

}



fetchEmpresas(1, null);