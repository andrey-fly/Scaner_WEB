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

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        dropArea.classList.add('highlight');
    }

    function unhighlight(e) {
        dropArea.classList.remove('highlight');
    }

    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        let dt = e.dataTransfer;
        let files = dt.files;

        handleFiles(files);
    }

    function handleFiles(files) {
        ([...files]).forEach(uploadFile);
    }

    function uploadFile(file) {
        let url = '/photo/';
        let formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrftoken);
        formData.append('file', file.name);
        fetch(url, {
            method: 'POST',
            body: formData,
        });
    }
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
    input.name = 'file';
    form.submit();
}