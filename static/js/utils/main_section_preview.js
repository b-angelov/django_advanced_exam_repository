
function toggleIfContent(element){
    if (element.innerHTML.trim()){
        // document.querySelector('#some').classList.
        element.classList.remove('disable-preview')
        return true;
    } else{
        element.classList.add('disable-preview')
        return false;
    }
}

export default function mainSectionToggle(){

    const section = document.querySelector('#component')
    let toggle = false;
    for (const child of Object.values(section.children)){
        if (toggleIfContent(child)){
            toggle = true;
        }
    }
    if (toggle){
        section.classList.remove('disable-preview')
    }else{
        section.classList.add('disable-preview')
    }
}