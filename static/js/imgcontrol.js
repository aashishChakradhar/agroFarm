function handleFileInputChange(evt, maxSizeKB, imgElementId, imgfieldelement ='') {
    var input = evt.target;
    var file = input.files[0];
    
    if (file) {
        var fileSize = file.size;
        var maxSize = maxSizeKB * 1024; // Convert KB to bytes
        
        if (fileSize > maxSize) {
            alert('File size exceeds ' + maxSizeKB + 'KB. Please choose a smaller file.');
            input.value = ''; // Clear the file input to reset
        } else {
            const imageElement = document.getElementById(imgElementId);
            imageElement.src = URL.createObjectURL(file);
            
            var reader = new FileReader();
            
            reader.onload = function(e) {
                input.dataset.blob = e.target.result;
                if(imgfieldelement != ''){
                    imgfieldelement.value = e.target.result;
                }
            };
            
            reader.readAsDataURL(file);
        }
    }
}

const profileImgInput = document.getElementById('profileimg');
const productImgInput = document.getElementById('productimg');
const producttypeImgInput = document.getElementById('producttypeimg');
const removeimg = document.getElementById('removeimg');
const fimg = document.getElementById('fimg')
const profileimgblob = document.getElementById('profileimgblob');
const productimgblob = document.getElementById('productimgblob');
const producttypeimgblob = document.getElementById('producttypeimgblob');

//profile image show on page on change using blob
if (profileImgInput) {
    profileImgInput.onchange = function(evt) {
        const [file] = profileImgInput.files
        if (file){
            handleFileInputChange(evt, 300, 'fimg', profileimgblob);
        }
    };
}
//product image show on page
if(productImgInput){
    productImgInput.onchange = evt => {
        const [file] = productImgInput.files
        if (file) {
            handleFileInputChange(evt, 300, 'fimg', productimgblob);
        }
    }
}

if(producttypeImgInput){
    producttypeImgInput.onchange = evt => {
        const [file] = producttypeImgInput.files
        if (file) {
            handleFileInputChange(evt, 300, 'fimg', producttypeimgblob);
        }
    }
}

if(removeimg){
    removeimg.addEventListener('click', (e) => {
        e.preventDefault();
        if(profileImgInput){
            profileImgInput.value = '';
            document.getElementById('fimg').setAttribute('src', 'http://matters.cloud392.com/wp-content/uploads/2024/06/camera-icon.png');
        }
        if(productImgInput){
            productImgInput.value = '';
            document.getElementById('fimg').setAttribute('src', 'http://matters.cloud392.com/wp-content/uploads/2024/06/camera-icon.png');
        }
        if(producttypeimgblob){
            producttypeimgblob.value = '';
            document.getElementById('fimg').setAttribute('src', 'http://matters.cloud392.com/wp-content/uploads/2024/06/camera-icon.png');
        }
    });
}
