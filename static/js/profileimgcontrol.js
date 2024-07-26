var profileImgInput = document.getElementById('profileimg');

if (profileImgInput) {
    profileImgInput.onchange = function(evt) {
        var input = evt.target;
        var file = input.files[0];
        
        if (file) {
            var fileSize = file.size;
            var maxSize = 30 * 1024; // 30 KB in bytes
            
            if (fileSize > maxSize) {
                alert('File size exceeds 30KB. Please choose a smaller file.');
                input.value = ''; // Clear the file input to reset
            } else {
                const imageElement = document.getElementById('fimg');
                imageElement.src = URL.createObjectURL(file);
                
                var reader = new FileReader();
                
                reader.onload = function(e) {
                    input.dataset.blob = e.target.result;
                };
                
                reader.readAsDataURL(file);
            }
        }
    };
}