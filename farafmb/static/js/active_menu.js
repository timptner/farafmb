document.addEventListener('DOMContentLoaded', () => {
    let element = document.querySelector('#adminNavigation');

    if (element !== null) {
        (element.querySelectorAll('a') || []).forEach((node) => {
            if (document.URL.startsWith(node.href)) {
                node.classList.add('is-active');
            }
        });
    }
});
