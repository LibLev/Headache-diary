function init(){
    let registerButton = document.getElementById('register-button');
    registerButton.addEventListener('click',function () {
        window.location.href = 'registration'
    });
}

init();