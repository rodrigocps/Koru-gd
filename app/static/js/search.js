function renderSearch() {
    document.getElementById("search-btn").addEventListener("click", (event) => {
        event.preventDefault()
        const search = document.getElementById("search").value

        
        if(search.length > 0 && !(/^[\s\t]*$/.test(search)) ) {
            const params = defParam("search", search)
            if(params.get("pagina")) params.set("pagina", 1)
            window.location.href = window.location.pathname + "?" + params.toString()
        }
        else {
            window.location.href = window.location.href
        }
    })
}