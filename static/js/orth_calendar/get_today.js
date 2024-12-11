
let element = document.querySelector('#component .component-wrapper')
const pattern = document.querySelector('#calendar-main') || null
if (pattern){
    element = pattern.parentElement
    pattern.remove()
}

import {htmlPatternParse, loadDateFeastAndSaints, todayFeastsAndSaints, toggleDescription} from "./date_feast_and_saints.js";


const funcs = [
    [todayFeastsAndSaints,[element,pattern]],
]

window.addEventListener('load', ()=> {
    for (const [func,params] of funcs){
        (async () => func(...params))();
    }
})