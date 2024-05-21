function renderSearch() {
    document.getElementById("search-btn").addEventListener("click", (event) => {
        event.preventDefault()
        const search = document.getElementById("search").value.trim()

        
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

document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const search = params.get("search") ? params.get("search") : null
    const byName = params.get("SEARCH_BY_NAME") ? "SEARCH_BY_NAME" : null
    const bySetor = params.get("SEARCH_BY_SETOR") ? "SEARCH_BY_SETOR" : null

    const searchBox = document.querySelector("#search-bar > input")
    const chckBoxName = document.getElementById("searchByName")
    const chckBoxSetor = document.getElementById("searchBySetor")

    if(searchBox && search) searchBox.value = search
    if(chckBoxName && byName) chckBoxName.checked = true
    if(chckBoxSetor && bySetor) chckBoxSetor.checked = true

    if(!byName && !bySetor) {
        chckBoxName.checked = true
        chckBoxSetor.checked = true
    }
})