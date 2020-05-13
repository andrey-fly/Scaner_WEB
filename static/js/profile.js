while (document.getElementById('rating').getElementsByClassName('active').length > 1) {
    document.getElementById('rating').getElementsByClassName('active')[1].classList.remove('active');
}
while (document.getElementById('goods').getElementsByClassName('active').length > 1) {
    document.getElementById('goods').getElementsByClassName('active')[1].classList.remove('active');
}

function preview_image(event) {
    var reader = new FileReader();
    reader.onload = function() {
        var output = document.getElementById('output_image');
        output.src = reader.result;
    }
    reader.readAsDataURL(event.target.files[0]);
}