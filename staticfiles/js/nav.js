
function Navigation(){
    const dropdowns = document.querySelectorAll('li.dropdown');

    for (let dropdown of dropdowns){
        const dropdownMenu = dropdown.querySelector(".dropdown-menu")

        dropdown.addEventListener("mouseover",(e)=>{
            dropdownMenu.style.display = "flex";
        })
        dropdown.addEventListener("mouseout",(e)=>{
            dropdownMenu.style.display = "none";
        })
    }
}
Navigation()