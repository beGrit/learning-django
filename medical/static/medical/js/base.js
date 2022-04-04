window.addEventListener('load', function () {
    const menuShowButton = document.querySelector('#components-show-button')
    const headerMenuElm = document.querySelector('#header-components')
    menuShowButton.onclick = function (e) {
        if (!headerMenuElm.classList.contains('header-components-hidden')) {
            headerMenuElm.classList.add('header-components-hidden')
        } else {
            headerMenuElm.classList.remove('header-components-hidden')
        }
    }
})
