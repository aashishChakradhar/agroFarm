document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function () {
            const productUid = this.dataset.productUid;

            fetch(`/add-to-cart/${productUid}/`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                return response.json().then(data => {
                    if (!response.ok) {
                        // Handle the error message from the server without throwing an error
                        console.error('Error response:', data);
                        window.alert(data.message || 'An unexpected error occurred.');
                        return; // Exit early for errors
                    }
                    return data; // Pass the success data to the next `.then()`
                });
            })
            .then(data => {
                if (data && data.success) {
                    // Success case: Product was added to the cart
                    window.alert(data.message); // Show success alert
                    const messageDiv = document.getElementById('success-message');
                    messageDiv.innerText = data.message;
                    messageDiv.style.display = 'block';
                    setTimeout(() => {
                        messageDiv.style.display = 'none';
                    }, 3000);

                    // Optionally update cart count in the UI
                    const cartCountSpan = document.getElementById('cart-count');
                    if (cartCountSpan) {
                        cartCountSpan.innerText = data.cart_count;
                    }
                }
            })
            .catch(error => {
                console.error('Unexpected error details:', error);
                window.alert('An unexpected error occurred. Please try again later.');
            });
        });
    });

    const selectAllCheckbox = document.getElementById('select');
    const form = document.getElementById('myForm');
    if(form){
        const checkboxes = form.querySelectorAll('input[name="cart_item"]');
    }

    if(selectAllCheckbox){
        selectAllCheckbox.addEventListener('change', function () {
            const isChecked = this.checked;
            checkboxes.forEach(checkbox => {
                checkbox.checked = isChecked;
            });
        });
    }

    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach((input) => {
        // Set initial price when the page loads
        const rateCell = input.closest('tr').querySelector('td:nth-child(3)');
        const priceCell = input.closest('tr').querySelector('td:nth-child(5)');

        const rate = parseFloat(rateCell.textContent);
        const quantity = parseFloat(input.value);

        if (!isNaN(rate) && !isNaN(quantity)) {
            const totalPrice = rate * quantity;
            priceCell.textContent = totalPrice.toFixed(2);
        }

        // Event listener for quantity change
        input.addEventListener('input', function () {
            const updatedQuantity = parseFloat(input.value);

            if (updatedQuantity < 1) {
                alert("Quantity must be at least 1.");
                input.value = 1; // Reset to 1 if less than 1
            }

            if (!isNaN(rate) && !isNaN(updatedQuantity)) {
                const totalPrice = rate * updatedQuantity;
                priceCell.textContent = totalPrice.toFixed(2);
            } else {
                priceCell.textContent = '';
            }
        });
    });

    document.querySelectorAll('.product-item .locationpoint').forEach( (element) => {
        element.addEventListener('click', (e) => {
            console.log(e.target.classList.toggle('active'));
        })
    })
});