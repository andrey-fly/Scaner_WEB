document.addEventListener("DOMContentLoaded", function(event) {
    let dropArea = document.getElementById('photo-frame-in-content-group');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults (e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        dropArea.classList.add('highlight');
    }

    function unhighlight(e) {
        dropArea.classList.remove('highlight');
    }

    dropArea.addEventListener('drop', handleDrop, false);

    func_element_hide();

    function handleDrop(e) {
        let dt = e.dataTransfer;
        let files = dt.files;

        handleFiles(files);
    }

    function handleFiles(files) {
        ([...files]).forEach(uploadFile);
    }

     async function uploadFile(file) {
        let url = '/';
        let formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrftoken);
        formData.append('file', file);
        let response = fetch(url, {
            method: 'POST',
            body: formData,
        });
        $('.loader').css('display', 'block');
        setTimeout(function(){
          $('.loader').fadeOut(700, function(){
            $(this).css('display', 'none');
          });
            }, 1500);

        let result = await response;

        if (result.redirected){
            window.location.href = result.url;
        }
    }
    window.addEventListener("resize", function() {func_element_hide();});
});

function func_submit_btn() {
    let form = document.getElementById("content-group");
    let input = document.getElementById("file-input-for-label");
    input.name = 'file';
    form.submit();
}

function func_submit_area() {
    let form = document.getElementById("content-group");
    let input = document.getElementById("file-input-for-frame");
    console.log('kek');
    input.name = 'file';
    form.submit();
}

function func_element_hide(){
    let dropSubmit = document.getElementById('file-input-for-frame');
    let dropArea = document.getElementById('photo-frame-in-content-group');
    if (window.innerWidth < 910){
        dropSubmit.style.display = 'none';
        dropArea.style.display = 'none';
    }
    else{
        dropSubmit.style.display = 'flex';
        dropArea.style.display = 'flex';
    }
}