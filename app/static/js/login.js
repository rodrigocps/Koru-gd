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
            if(!response.ok) {
                throw new Error("Erro ao efetuar o login do usuário.")
            }
            
            window.location.href = "/"
        }).catch(error => console.log(error))
    });

    /*
    
    document.getElementById("signupBtn").addEventListener('click', (event) => {
        event.preventDefault();

        window.location.href = "/signup"
    })

    */

  });