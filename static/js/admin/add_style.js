
function add_style(){
    const helptexts = document.querySelectorAll("textarea");
    for (const text of helptexts){
        const next_sbl = text.nextElementSibling;
        next_sbl.style.fontStyle = 'italic';
        next_sbl.style.fontSize = '0.7em';
        next_sbl.style.color = 'rgba(19,141,62,0.8)';
        text.style.border = 'solid 1px rgb(121,211,214,0.2)';
        text.setAttribute('x-bind:class',"adminTheme === 'dark' ? 'bg-gray-900' : 'bg-white'")
        text.addEventListener('focus',(e)=>{
            e.currentTarget.style.outline = '2px solid rgba(19,141,62,0.6)';
        })
        text.addEventListener('focusout', e =>{
            e.currentTarget.style.outline = '0px none';
        })
        text.parentNode.insertBefore(next_sbl, text);
    }
}

window.addEventListener('load',add_style)