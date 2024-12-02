import mainSectionToggle from "./utils/main_section_preview.js";

const functions_list = [
    [mainSectionToggle,[]],
]

function JsExecutionOrder(){
    for (const [func, values] of functions_list){
        func(...values)
    }
}

window.addEventListener('load', JsExecutionOrder)