document.addEventListener('DOMContentLoaded', function() {
  document.getElementById("signupBtn").addEventListener("click", (event) => {
    event.preventDefault();
    submitForm();
  })
})

function submitForm() {
    // Pega os valores dos campos do formulário
    var nome = document.getElementById("nome").value;
    var email = document.getElementById("email").value;
    var senha = document.getElementById("senha").value;
  
    // Cria um objeto com os dados a serem enviados para a API
    var formData = {
        nome: nome,
        email: email,
        senha: senha
    };
  
    // Envia os dados para a API usando fetch
    fetch('/api/usuarios', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
    .then(response => {
      if (!response.ok) {
        // tratamento do erro
        throw new Error('Erro ao cadastrar o usuário.');
      }
      return response.json();
    })
    .then(data => {
        window.location.href = "/"
    })
    .catch(error => {
      console.error('Erro:', error);
    });
  }