function init(){
    let registerButton = document.getElementById('register-button');
    registerButton.addEventListener('click',function () {
        window.location.href = 'registration'
    });
    let confirmationButton = document.getElementById('registration-confirmation');
    confirmationButton.addEventListener('click', function () {
        window.location = 'login.html'
    })
}

init();