document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('submitBtn').addEventListener('click', function(event) {
        event.preventDefault()

        const formData = {
            email : document.getElementById("email").value,
            senha : document.getElementById("senha").value
        }

        fetch("/api/usuarios/auth", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        }).then(response => {
            const errorElement = document.getElementById("error")

            if(response.status === 401 || response.status === 422) {
                errorElement.textContent = "Email ou senha inválidos."
            } else if(!response.ok) {
                errorElement.textContent = "Ocorreu um erro interno ao processar sua solicitação."
            }
            else window.location.href = "/"

        }).catch(error => {
            const errorElement = document.getElementById("error")
            errorElement.textContent = "Ocorreu um erro interno ao processar sua solicitação."
        })
    });
  });