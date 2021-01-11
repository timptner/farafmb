document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.file.has-name') || []).forEach(($field) => {
        let $input = $field.querySelector('input');
        let $output = $field.querySelector('.file-name');

        $input.addEventListener('change', () => {
            $output.textContent = $input.value.split('\\').pop();
        });
    });
});