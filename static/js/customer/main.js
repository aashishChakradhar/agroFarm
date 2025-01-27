document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const productUid = this.dataset.productUid;
            const quantity = this.dataset.quantity;
            const farmer = this.dataset.farmer;

            fetch(`/add-to-cart/${productUid}/?quantity=${quantity}&farmer=${farmer}`, {
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

    const quantityInputs = document.querySelector('input[name="quantity"]');
    if(quantityInputs){
        quantityInputs.addEventListener('change', (e) => {
            if(document.querySelector('.add-to-cart-btn')){
                document.querySelector('.add-to-cart-btn').setAttribute('data-quantity', e.target.value);
            }
        })
    }

    // if (document.querySelector('.checkout-table')) {
    //     const tableRows = document.querySelectorAll('.checkout-table tbody tr');
    //     tableRows.forEach((row) => {
    //         const rate = parseFloat(row.querySelector('.rate').textContent);
    //         const finalPrice = row.querySelector('.total');
    //         const quantity = row.querySelector('input[name="quantity"]');
    //         function priceChange(){
    //             if (quantity.value < 1) {
    //                 alert("Quantity must be at least 1.");
    //                 quantity.value = 1;
    //             }
    //             finalPrice.textContent = (rate * quantity.value).toFixed(2);
    //         }
    //         priceChange();
    //         quantity.addEventListener('input',()=>{
    //             priceChange();
    //         });
    //         quantity.addEventListener('change',()=>{
    //             priceChange();
    //         });
    //     });
    // }

    document.querySelectorAll('.product-listing-stock').forEach(function (element) {
        element.addEventListener('click', (e) => {
            if (e.target.classList.contains('locationpoint')) {
                if (e.target.classList.contains('active')) {
                    e.target.classList.remove('active');
                    e.target.classList.remove('active-success');
                    document.querySelector('.out-of-area-msg').style.display = 'none';
                } else {
                    element.querySelectorAll('.locationpoint').forEach(function (child) {
                        child.classList.remove('active');
                        child.classList.remove('active-success');

                    });
                    e.target.classList.add('active');
                    document.querySelector('.add-to-cart-btn').setAttribute('data-farmer', e.target.getAttribute('data-farmerid'));
                    if(e.target.classList.contains('out-of-area')){
                        document.querySelector('.out-of-area-msg').style.display = 'block';
                    }else{
                        e.target.classList.add('active-success');
                        document.querySelector('.out-of-area-msg').style.display = 'none';
                    }1
                }
            }
        });
    });

    document.querySelectorAll('.product-item .locationpoint').forEach( (element) => {
        element.addEventListener('click', (e) => {

            if(e.target.classList.contains('active')){
                if(document.querySelector('.add-to-cart-btn')){
                    document.querySelector('.add-to-cart-btn').setAttribute('data-farmer', e.target.getAttribute('data-farmerid'));
                }
            }
        })
    })

    function buybuttondisabler(b){
        document.querySelectorAll('#buyform button').forEach((element) => {
            element.disabled = b;
        });
    }
    function checkConditions() {
        const quantity = document.getElementById('quantity').value;
        const locationSelected = document.querySelector('.locationpoint.active-success') !== null;

        if (quantity > 0 && locationSelected) {
            buybuttondisabler(false);
        }else {
            buybuttondisabler(true);
        }
    }

    if(document.querySelector('.okbtn')){
        document.querySelector('.okbtn').addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelectorAll('.locationpoint.active').forEach((item) => {
                item.classList.add('active-success');
            })
            document.querySelector('.out-of-area-msg').style.display = 'none';
        })
    }

    if(document.querySelector('.cancelbtn')){
        document.querySelector('.cancelbtn').addEventListener('click', (e) => {
            e.preventDefault();

            document.querySelectorAll('.locationpoint.out-of-area.active').forEach((element) => {
                element.classList.remove('active');
            });

            document.querySelector('.out-of-area-msg').style.display = 'none';
        })
    }
    if(document.querySelector('.detail-content-wrapper')){
        document.querySelector('.detail-content-wrapper').addEventListener('click',()=>{
            checkConditions();
        })
    }
    if(document.getElementById('quantity')){
        document.getElementById('quantity').addEventListener('change', () => {
            checkConditions();
        });
    }

    if(document.querySelectorAll('.my-cart-table')){
        let checkboxs = document.querySelectorAll('.my-cart-table tbody input[type="checkbox"]');
        if(document.querySelector('.my-cart-table #cartSelectAll')){
            document.querySelector('.my-cart-table #cartSelectAll').addEventListener('click',function(){
                const isChecked = this.checked;
                checkboxs.forEach(checkbox => {
                    checkbox.checked = isChecked;
                });
            });
        }
        checkboxs.forEach(checkbox => {
            checkbox.addEventListener('change',()=>{
                document.querySelector('.my-cart-table #cartSelectAll').checked = false;
            });
        });
    }

    const checkboxes = document.querySelectorAll('.my-cart-table input[name="cart_item"]');
    if(checkboxes){
        checkboxes.forEach((item)=>{
            item.addEventListener('change', (e) => {
                const farmerItem = e.target.closest('label').querySelector('input[name="farmer_item"]');
                const quantityItem = e.target.closest('label').querySelector('input[name="quantity_item"]');
                farmerItem.checked = e.target.checked;
                quantityItem.checked = e.target.checked;
                let isAnyChecked = Array.from(checkboxes).some(i => i.checked);

                if (isAnyChecked) {
                    document.querySelector('.buynowbtn').disabled = false;
                    document.querySelector('.deleteitembtn').disabled = false;
                } else {
                    document.querySelector('.buynowbtn').disabled = true;
                    document.querySelector('.deleteitembtn').disabled = true;
                }
            })
        });
    }

    document.querySelectorAll('input[name="quantity"]').forEach((element) => {
        element.addEventListener('change', (e) => {
            if(e.target.closest('tr')){
                e.target.closest('tr').querySelector('input[name="quantity_item"]').value = e.target.value;
            }
        })
    })

    if (document.querySelector('.checkout-table')) {
        const tableRows = document.querySelectorAll('.checkout-table tbody tr');
        tableRows.forEach((row) => {
            const rate = parseFloat(row.querySelector('.rate').textContent);
            const finalPrice = row.querySelector('.total');
            const quantity = row.querySelector('.quantity-num');

            finalPrice.textContent = (rate * quantity.textContent).toFixed(2);
        });
    }
});