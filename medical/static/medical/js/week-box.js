window.addEventListener('load', function () {
    const liList = document.querySelectorAll('#nav-week-list li')
    for (let li of liList) {
        li.addEventListener('click', function (e) {
            if (!li.classList.contains('crt')) {
                document.querySelector('.crt').classList.remove('crt')
                li.classList.add('crt');
            }
        })
    }
})
