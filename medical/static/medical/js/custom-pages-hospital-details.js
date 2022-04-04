window.addEventListener('load', function () {
    const description_content = document.querySelector('.hospital-details .description-info .description-content')
    const btn = document.querySelector('.hospital-details .description-info .about-more .about-more-btn')
    btn.addEventListener('click', function () {
        if (description_content.classList.contains('text-over-hidden')) {
            description_content.classList.remove('text-over-hidden')
            btn.textContent = '收纳'
        } else {
            description_content.classList.add('text-over-hidden')
            btn.textContent = '展开所有'
        }
    })
})