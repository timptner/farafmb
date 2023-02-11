document.addEventListener('DOMContentLoaded', () => {
    let element = document.querySelector('div.tabs');

    if (element) {
        (element.querySelectorAll('li') || []).forEach((node) => {
            if (node.querySelector('a').href === document.URL) {
                node.classList.add('is-active');
            }
        });
    }
});
