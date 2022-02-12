window.onload = function () {
    const menuShowButton = document.querySelector('#menu-show-button')
    const headerMenuElm = document.querySelector('#header-menu')
    menuShowButton.onclick = function (e) {
        if (!headerMenuElm.classList.contains('header-menu-hidden')) {
            headerMenuElm.classList.add('header-menu-hidden')
        } else {
            headerMenuElm.classList.remove('header-menu-hidden')
        }
    }
}
