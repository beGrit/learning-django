window.onload = function (e) {
    const send_code = document.querySelector('#send-code');
    let form_data = new FormData(document.querySelector('#login-email-form'));
    send_code.addEventListener('click', (e) => {
        let email = form_data.get('email');
        let path = 'login/email/send_code/' + email;
        fetch(path, {
            'method': 'get',
        }).then(function (result) {
            console.log(result.json())
        })
    });
}