
export default function handleLogout(){
    const button = document.querySelector('a[href*="/auth/logout/"]')
    if (!button){
        return
    }
    button.addEventListener('click',e=>{
        e.preventDefault();
        (async ()=>{
            // let res =await fetch('/auth/logout/',{
            //     method:'POST',
            //     headers: {
            //         "Content-Type": "application/json",
            //         "X-CSRFToken": document.cookie.split('=')[1]// Include CSRF token in header
            //     },
            //     body:JSON.stringify({
            //     })
            // })

            const form = document.querySelector('#logout-form')
            form.submit()

            // document.location.href = res.url

        })();
    })
}

