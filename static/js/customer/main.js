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
});
