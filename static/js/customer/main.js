document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const productUid = this.dataset.productUid;
            const quantity = this.dataset.quantity;
            const farmer = this.dataset.farmer;
            const distance = this.dataset.distance;

            fetch(`/add-to-cart/${productUid}/?quantity=${quantity}&farmer=${farmer}&distance=${distance}`, {
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

            document.querySelectorAll('.locationpoint').forEach( (item) => {
                let quantity = item.querySelector('.farmer-quantity').textContent.trim();
                if(parseInt(e.target.value) > parseInt(quantity)){
                    item.style.display = 'none';
                }else{
                    item.style.display = 'block';
                }
            })
        })
    }

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
                    document.querySelector('.add-to-cart-btn').setAttribute('data-distance', e.target.getAttribute('data-distance'));
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
                    document.querySelector('.add-to-cart-btn').setAttribute('data-distance',e.target.getAttribute('data-distance'));
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
                const distance = e.target.closest('label').querySelector('input[name="distance"]');
                farmerItem.checked = e.target.checked;
                quantityItem.checked = e.target.checked;
                distance.checked = e.target.checked;
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

    if(document.querySelector('.delivery-payment')){
        const distance = document.querySelector('.delivery-payment').getAttribute('data-distancebet');
        if(distance > 5){
            let d = distance, b = 0, i = 0;
            while(d>0){
                d = d-10;
                i++;
                if(d < 10){
                    b = d;
                    break;
                }
            }
            let amt = (60*i + (6*d));
            document.querySelector('input[name="deliveryprice"]').value = amt.toFixed(2);
            document.querySelector('.delivery-amount').innerHTML = `Rs. ${amt.toFixed(2)}`;
            
        }else{
            document.querySelector('input[name="deliveryprice"]').value = 0;
            document.querySelector('.delivery-amount').innerHTML = 'Free Delivery';
        }
    }
    if(document.querySelector('.subtotal')){
        const deliverycharge = parseFloat(document.querySelector('input[name="deliveryprice"]').value);

        let productprice = 0;
        document.querySelectorAll('.total').forEach((item) => {
            productprice += parseFloat(item.innerHTML);
        })

        let subtotal = productprice + deliverycharge;
        document.querySelector('.subtotal').innerHTML = `Rs. ${subtotal}`;
    }

    //select only one item from cart
    let cartRow = document.querySelectorAll('.my-cart-table input[name="cart_item"]');
    cartRow.forEach(function(element, index) {
        element.addEventListener('change', function() {
            cartRow.forEach(function(ele, index2) {
                if (index !== index2) {
                    ele.disabled = element.checked; // Disable others if the current one is checked
                } else {
                    ele.disabled = false; // Keep the selected one enabled
                }
            });
        });
    });

    //Farmer sorting
    let container = document.querySelector(".product-listing-stock");
    let items = Array.from(document.querySelectorAll(".product-item"));

    // Sort items: Those without .out-of-area come first
    items.sort((a, b) => {
        let aOutOfArea = a.querySelector(".locationpoint").classList.contains("out-of-area") ? 1 : 0;
        let bOutOfArea = b.querySelector(".locationpoint").classList.contains("out-of-area") ? 1 : 0;
        return aOutOfArea - bOutOfArea;
    });

    // Append sorted items back to the container
    items.forEach(item => container.appendChild(item));
});