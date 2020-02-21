document.addEventListener("DOMContentLoaded", function(event) {
    let dropZone = document.querySelector("#photo-frame-in-content-group");

    dropZone.addEventListener("drag dragstart dragend dragover dragenter dragleave drop", function() {
        return false;
    });

    dropZone.addEventListener("dragover dragenter", function() {
        dropZone.classList.add('dragover');  // fix it
    });

    dropZone.addEventListener("dragleave", function(e){
        let dx = e.pageX - dropZone.offset.left;  //fix it
        let dy = e.pageY - dropZone.offset.top;
        if ((dx < 0) || (dx > dropZone.width()) || (dy < 0) || (dy > dropZone.height())) {
            dropZone.classList.remove('dragover');
        }
    });

    dropZone.addEventListener('drop', function(e) {
        dropZone.classList.remove('dragover');
		let files = e.originalEvent.dataTransfer.files;
		sendFiles(files);
    });

    document.querySelector('#file-input').change(function(){
        let files = this.files;
		sendFiles(files);
    });

    function sendFiles(files) {  //fix it
		let maxFileSize = 5242880;
		let Data = new FormData();
		Array.prototype.forEach.call(document.querySelectorAll(files), function(index, file){
			if ((file.size <= maxFileSize) && ((file.type == 'image/png') || (file.type == 'image/jpeg'))) {
				Data.append('images[]', file);
			}
	    });
	}
});