document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.file.has-name') || []).forEach(($field) => {
        let $input = $field.querySelector('input[type=file]');
        let $output = $field.querySelector('.file-name');
        $input.onchange = () => {
            if ($input.files.length > 0) {
                $output.textContent = $input.files[0].name;
            }
        }
    });
});
