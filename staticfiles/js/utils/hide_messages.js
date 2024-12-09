
export default function hideMessages(){
    const messages = document.querySelector('.message-container');
    setTimeout(()=>messages.classList.toggle('hides'),4000)
}