import mainSectionToggle from "../utils/main_section_preview.js";
import {get} from "./calendar_fetchery.js"

export {htmlPatternParse, loadDateFeastAndSaints, todayFeastsAndSaints, toggleDescription}


function htmlPatternParse(element, data, pattern, override_pattern =true){
    const patt = pattern ? pattern.cloneNode(true) : document.createDocumentFragment();
    const resList = [];
    for (let [name,entry] of Object.entries(data)){
        if (typeof entry !== 'object'){
            entry = [entry]
        }
        for (const ent of entry) {
            const qname = patt.querySelector(`.${name}`)
            let el;
            if (qname){
                el = qname;
            }else if(override_pattern){
                el = document.createElement('div');
                patt.appendChild(el)
            }else{
                continue;
            }
            const p = document.createElement('p')
            p.textContent = ent.name || ent
            el.appendChild(p)
        }
    }
    element.insertBefore(patt,element.firstChild)

}

function loadDateFeastAndSaints(element,pattern,date){
    async function getDateObjects(){
        const data = await get(
            'holidays',
            {'by_date': date, 'related':1}
        )
        htmlPatternParse(element,data,pattern,false)
    }
    getDateObjects().then(r => mainSectionToggle()).then(r => toggleDescription())
}



function todayFeastsAndSaints(element,pattern){
    const currentDate = new Date().toJSON().slice(0,10)
    loadDateFeastAndSaints(element,pattern,currentDate)
}

function toggleDescription(){
    const description = document.querySelectorAll('#calendar-main .desc')
    console.log(description)
    for (const desc of description.values()){
        console.log(desc)
        if (!desc.previousElementSibling && !desc.nextElementSibling){
            desc.style.visibility = 'hidden';
        }
    }
}

