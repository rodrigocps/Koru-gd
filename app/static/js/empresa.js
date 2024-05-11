const params = new URLSearchParams(window.location.search);

const id = params.get('id');

if(id) {
    fetch("/empresas/" + id)
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