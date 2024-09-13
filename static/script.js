// Select the file input and the iframe for document preview
const uploadInput = document.getElementById('uploadInput');
const documentPreview = document.getElementById('documentPreview');

// Event listener for file upload input
uploadInput.addEventListener('change', function () {
    const file = uploadInput.files[0];

    if (file) {
        const fileURL = URL.createObjectURL(file);
        documentPreview.src = fileURL;
    }
});