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
            if(data.logo_url) {
                const logo = document.getElementById("logo-empresa")
                logo.src = data.logo_url
            }

            const pageTitle = document.querySelector("head > title")
            pageTitle.textContent = data.nome + " - Koru Jobs"

            nome.textContent = data.nome
            setor.textContent = data.setor
            
        }).catch(error => console.log(error))

        
}