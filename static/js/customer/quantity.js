document.addEventListener('DOMContentLoaded', () => {
    //Quantity JS
    // Add event listeners to handle the quantity changes
    document.querySelectorAll('.quantity').forEach(function (spinner) {
        const input = spinner.querySelector('input[type="number"]');
        const btnUp = spinner.querySelector('.quantity-up');
        const btnDown = spinner.querySelector('.quantity-down');
        const step = parseFloat(input.getAttribute('step')) || 1;
        const min = parseFloat(input.getAttribute('min')) || 0;
        const max = parseFloat(input.getAttribute('max')) || 1000;
        // Event listener for the up button
        btnUp.addEventListener('click', function () {
            const oldValue = parseFloat(input.value) || 0;
            const newVal = oldValue >= max ? oldValue : oldValue + step;
            input.value = newVal;
            input.dispatchEvent(new Event('change'));
        });
        // Event listener for the down button
        btnDown.addEventListener('click', function () {
            const oldValue = parseFloat(input.value) || 0;
            const newVal = oldValue <= min ? oldValue : oldValue - step;
            input.value = newVal;
            input.dispatchEvent(new Event('change'));
        });
    });
})