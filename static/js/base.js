(() => {
    'use strict'
    document.querySelector('#offcanvasToggler').addEventListener('click', () => {
        document.querySelector('.offcanvas-collapse').classList.toggle('open')
    })
})()

document.querySelector('#navbar-file-choose').addEventListener('change', function () {
    document.querySelector('#navbar-file-choose-form').submit();
})

document.querySelector('#instruction-file-choose').addEventListener('change', function () {
    document.querySelector('#instruction-file-choose-form').submit();
})
