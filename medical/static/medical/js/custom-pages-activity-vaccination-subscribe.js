window.addEventListener('load', function () {
    let liList = document.querySelectorAll('#nav-week-list li')
    for (let li of liList) {
        li.addEventListener('click', function (e) {
            let id = li.getAttribute('id')
            let keyNumber = id.charAt(2)
            const table = document.querySelector('.mz_ta_'.concat(keyNumber))
            if (!table.classList.contains('table_show')) {
                const current_show_table = document.querySelector('.mz_ta.table_show')
                current_show_table.classList.remove('table_show')
                current_show_table.classList.add('none')
                table.classList.add('table_show')
                table.classList.remove('none')
            }
        })
    }

    const subscribe_btn = document.querySelector('.subscribe-btn')
    subscribe_btn.addEventListener('click', () => {
        let url = subscribe_btn.getAttribute('value')
        window.open(url)
    })
})