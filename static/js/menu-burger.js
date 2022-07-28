document.addEventListener('DOMContentLoaded', () => {

    // Get all "menu-burger" elements
    const $menuBurgers = Array.prototype.slice.call(document.querySelectorAll('.menu-burger'), 0);

    // Check if there are any menu burgers
    if ($menuBurgers.length > 0) {

        // Add a click event on each of them
        $menuBurgers.forEach( el => {
            el.addEventListener('click', () => {

                // Get the target from the "data-target" attribute
                const target = el.dataset.target;
                const $target = document.getElementById(target);

                // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
                el.classList.toggle('is-active');
                el.childNodes.forEach(node => {
                    if (node.nodeName === 'SPAN') {
                        node.classList.toggle('is-hidden');
                    }
                });
                $target.classList.toggle('is-active');

            });
        });

    }

});
