
export default function linkToImage(){
    let imagel = document.querySelector('label[for=id_image]')
    if (imagel){
        imagel = imagel.parentElement.querySelector('a')
        const link = imagel.getAttribute('href')
        imagel.textContent = "";
        const img = document.createElement('img')
        img.src = link
        img.setAttribute("style","max-width:20vw; max-height:20vh;")
        imagel.appendChild(img)
    }
}