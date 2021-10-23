document.addEventListener('DOMContentLoaded', () => {
    let html = document.querySelector('html');
    let button = document.querySelector('#modal-delete-button');
    let modal = document.querySelector('#' + button.dataset['target']);

    button.addEventListener('click', () => {
        html.classList.add('is-clipped');
        modal.classList.add('is-active');
    });

    modal.querySelector('.modal-background').addEventListener('click', () => {
        closeModal();
    });
    modal.querySelector('.modal-close').addEventListener('click', () => {
        closeModal();
    });

    function closeModal() {
        html.classList.remove('is-clipped');
        modal.classList.remove('is-active');
    }
});
