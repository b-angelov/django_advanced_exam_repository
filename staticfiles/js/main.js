import mainSectionToggle from "./utils/main_section_preview.js";
import handleLogout from "./utils/logout.js";
import hideMessages from "./utils/hide_messages.js";

const functions_list = [
    [mainSectionToggle,[]],
    [handleLogout,[]],
    [hideMessages,[]],
]

function JsExecutionOrder(){
    for (const [func, values] of functions_list){
        (async () =>
        func(...values))();
    }
}

window.addEventListener('load', JsExecutionOrder)