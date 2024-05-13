document.addEventListener('DOMContentLoaded', function() {
  document.getElementById("signupBtn").addEventListener("click", (event) => {
    event.preventDefault();
    const form = validarForm();
    if(form) submitForm(form);
  })
})

function validarForm() {
  const nome = document.getElementById("nome").value;
  const email = document.getElementById("email").value;
  const senha = document.getElementById("senha").value;

  let isFormValid = false

  const nomeFeedback = document.getElementById("nome-feedback")
  if(!nome || !validLength(nome, 2, 100)) {
    nomeFeedback.textContent = "O nome de usuário precisa conter no mínimo 2 caracteres, e no máximo 100 caracteres."
    setInputInvalid(nomeFeedback)
    isFormValid = false
  } else {
    nomeFeedback.textContent = ""
    setInputValid(nomeFeedback)
    isFormValid = true
  }

  const emailFeedback = document.getElementById("email-feedback")
  if(!validLength(email, 8, 256)) {
    emailFeedback.textContent = "Email inválido. A quantidade mínima de caracteres é 8."
    setInputInvalid(emailFeedback)
    isFormValid = false
  }
  else if(!validarEmail(email)) {
    emailFeedback.textContent = "Email inválido."
    setInputInvalid(emailFeedback)
    isFormValid = false
  }
  else {
    emailFeedback.textContent = "Email válido."
    setInputValid(emailFeedback)
    isFormValid = true
  }

  const senhaFeedback = document.getElementById("senha-feedback")
  if(!validLength(senha, 8, 256)) {
    senhaFeedback.textContent = "Senha inválida. A quantidade mínima de caracteres é 8"
    setInputInvalid(senhaFeedback)
    isFormValid = false
  }
  else {
    senhaFeedback.textContent = "Senha válida."
    setInputValid(senhaFeedback)
    isFormValid = true
  }

  console.log("form valido: ", isFormValid)
  if(isFormValid)
    return  {
        nome: nome,
        email: email,
        senha: senha
    };

  else return false

}

function validarEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

function submitForm(formData) {
    fetch('/api/usuarios', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
    .then(response => {
      const errorElement = document.getElementById("error")
      if (response.status === 400) {
        const mensagem = JSON.parse(response.json())
        console.log(mensagem)
        if(Object.keys(mensagem).includes("mensagem")) {
          errorElement.textContent = mensagem.mensagem
        }
        else {
          errorElement.textContent = "Ocorreu um erro ao cadastrar o seu usuário."
        }
        return false
      }
      else if(!response.ok) {
        errorElement.textContent = "Ocorreu um erro ao cadastrar o seu usuário."
        return false
      }
      
      else return response.json();
    })
    .then(data => {
        if(data) window.location.href = "/"
    })
    .catch(error => {
      const errorElement = document.getElementById("error")
      errorElement.textContent = "Ocorreu um erro ao cadastrar o seu usuário."
    });
}

function validLength(text, minLength, maxLength) {
  if(text.length < minLength || text.length > maxLength) return false;
  return true
}

function setInputValid(feedbackElement) {
  feedbackElement.classList.remove("invalid-input")
  feedbackElement.classList.add("valid-input")
}


function setInputInvalid(feedbackElement) {
  feedbackElement.classList.remove("valid-input")
  feedbackElement.classList.add("invalid-input")
}