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
    fetch('http://127.0.0.1:5000/usuarios', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
    .then(response => {
      if (!response.ok) {
        // tratamento do erro
        throw new Error('Erro ao enviar o formulário');
      }
      return response.json();
    })
    .then(data => {
        
        // redirecionar para pagina logada
    })
    .catch(error => {
      console.error('Erro:', error);
    });
  }