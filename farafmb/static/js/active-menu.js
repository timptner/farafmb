document.addEventListener('DOMContentLoaded', () => {

    let menu = document.querySelector('#admin-nav');

    (menu.querySelectorAll('a') || []).forEach(($element) => {
        if ($element.href === document.URL) {
            $element.classList.add('is-active');
        }
    });
});
