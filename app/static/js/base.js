function renderAuthenticated(user){
    console.log("authenticated")
    const authButton = document.getElementById("auth-button");
    authButton.className = "logout-button"
    authButton.textContent = "Sair"
    authButton.addEventListener("click" , (event) => {
        event.preventDefault()
        fetch("/api/usuarios/logout", {
            method: "POST"
        }).then(response => {
            if(!response.ok) {
                throw new Error("Erro ao deslogar o usuário.")
            }
            logoutUser()
        }).catch(error => {
            console.log(error)
        })
    })

    if(user) {
        const userName = document.getElementById("user-name");
        userName.textContent = user?.nome ?? ""

        const navBar = document.querySelector("ul.navbar-nav");
        // <a class="nav-link mx-lg-2 active" aria-current="page" href="/">Início</a>
        const profileItem = document.createElement("a")
        profileItem.classList.add("nav-link", "mx-lg-2", "active")
        profileItem.ariaCurrent = "page"
        profileItem.href = "/perfil"
        profileItem.textContent = "Perfil"

        const li = document.createElement("li")
        li.classList.add("nav-item")
        li.append(profileItem)

        navBar.append(li)
    }
}

function renderNotAuthenticated(){
    console.log("not authenticated")
    const authButton = document.getElementById("auth-button");
    authButton.className = "login-button"
    authButton.href = "/login"
    authButton.textContent = "Login"
}

function validateLogin() {
    fetch("/api/usuarios/validate")
        .then(response => {
            if (response.status === 401) {
                localStorage.setItem("user", null)
                renderNotAuthenticated();
                return false
            }
            else if (response.ok)
                return response.json(); // Retorna uma promessa para o JSON
            else
                throw new Error("Erro ao enviar solicitação de validação de usuário.");
            
        })
        .then(data => {
            if(data) {
                localStorage.setItem("user", JSON.stringify(data))
                renderAuthenticated(data);
            }
        })
        .catch(error => {
            console.error("Erro durante a validação de login:", error);
        });
}

function logoutUser() {
    localStorage.setItem("user", null)
    window.location.href = window.location.pathname + window.location.search
}


document.addEventListener('DOMContentLoaded', function() {
    if(window.location.pathname !== "/login")
        validateLogin();
});

