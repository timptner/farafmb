document.addEventListener('DOMContentLoaded', () => {
    // Functions to open and close a modal
    function openModal(element) {
        element.classList.add('is-active');
    }

    function closeModal(element) {
        element.classList.remove('is-active');
    }

    function closeAllModals() {
        (document.querySelectorAll('.modal') || []).forEach((node) => {
            closeModal(node);
        });
    }

    // Add a click event on buttons to open a specific modal
    (document.querySelectorAll('.js-modal-trigger') || []).forEach((trigger) => {
        const modal = trigger.dataset.target;
        const target = document.getElementById(modal);

        trigger.addEventListener('click', () => {
            openModal(target);
        });
    });

    // Add a click event on various child elements to close the parent modal
    (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach((node) => {
        const target = node.closest('.modal');

        node.addEventListener('click', () => {
            closeModal(target);
        });
    });

    // Add a keyboard event to close all modals  DEPRECATED JS
    // document.addEventListener('keydown', (event) => {
    //     const e = event || window.event;
    //
    //     if (e.keyCode === 27) { // Escape key
    //         closeAllModals();
    //     }
    // });
});
