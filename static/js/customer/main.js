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
            e.target.classList.toggle('active');
        })
    })

    // document.querySelector('#buyform').addEventListener('submit', (e) => {
    //     e.preventDefault();
    //     let res = false;
    //     document.querySelectorAll('.active').forEach( (element) => {
    //         if(element.classList.contains('out-of-area')){
    //             res = confirm("One of the farmers you selected is located farther from your area. As a result, the delivery time may vary depending on the farmer's location, and the costs may be adjusted based on the distance.\n\nIf you want to continue click on 'OK'.");
    //         }
    //     });
    //     if(!res){
    //         return;
    //     }

    //     document.querySelector('button[name="action"]').value = 'buy';
    //     e.target.submit();
    //     // e.target.submit();
    // })

    function buybuttondisabler(b){
        document.querySelectorAll('#buyform button').forEach((element) => {
            element.disabled = b;
        });
    }
    function checkConditions() {
        const quantity = document.getElementById('quantity').value;
        const locationSelected = document.querySelector('.locationpoint.active') !== null;

        if (quantity > 0 && locationSelected) {
            buybuttondisabler(false);
        } else {
            buybuttondisabler(true);
        }
    }
    
    if(document.getElementById('quantity')){
        document.getElementById('quantity').addEventListener('change', () => {
            checkConditions();
        });
    }
    
    if(document.querySelectorAll('.locationpoint')){
        document.querySelectorAll('.locationpoint').forEach((element) => {
            element.addEventListener('click', (e) => {
                checkConditions();
            });
        });
    }
});