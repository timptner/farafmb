document.addEventListener('DOMContentLoaded', () => {

    let menu = document.querySelector('#navbarNavigation');

    (menu.querySelectorAll('a.navbar-item') || []).forEach(($element) => {
        if ($element.href === document.URL) {
            $element.classList.add('is-active');

            let dropdown = $element.parentElement
            if (dropdown.classList.contains('navbar-dropdown')) {
                dropdown.previousElementSibling.classList.add('is-active');
            }
        }
    });
});
