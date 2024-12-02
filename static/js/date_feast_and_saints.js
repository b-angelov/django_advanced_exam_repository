import mainSectionToggle from "./utils/main_section_preview.js";


function loadDateFeastAndSaints(){
    const currentDate = new Date().toJSON().slice(0,10)
    const outputElement = document.querySelector('#component .component-wrapper')
    async function getDateObjects(){
        const url = 'http://' + window.location.host + '/orth_calendar/holidays/'+currentDate+'?related=1'
        let data = await fetch(url)
        data = await data.json()
        for (let [name,entry] of Object.entries(data)){
            if (typeof entry !== 'object'){
                entry = [entry]
            }
            for (const ent of entry) {
                const paragraph = document.createElement('p')
                paragraph.textContent = ent.name || ent
                console.log(ent)
                outputElement.appendChild(paragraph)
            }
        }
    }
    getDateObjects().then(r => mainSectionToggle())
}

window.addEventListener('load', loadDateFeastAndSaints)