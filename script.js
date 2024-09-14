const uploadInput = document.getElementById('uploadInput');
const documentPreview = document.getElementById('documentPreview');

// Event listener for file upload input
uploadInput.addEventListener('change', function () {
    const file = uploadInput.files[0];

    if (file) {
        // Check if the file is a PDF, JPG, or PNG
        const fileType = file.type;

        if (fileType === 'application/pdf') {
            // Create a URL for the PDF file and display it in the iframe
            const fileURL = URL.createObjectURL(file);
            documentPreview.src = fileURL;
        } else if (fileType === 'image/jpeg' || fileType === 'image/png') {
            // For images (jpg, png), display in iframe
            const fileURL = URL.createObjectURL(file);
            documentPreview.src = fileURL;
        } else {
            // Alert if file type is unsupported
            alert('Unsupported file type. Please upload a PDF, JPG, or PNG file.');
            documentPreview.src = ''; // Clear iframe content
        }

        // Revoke the object URL after file is loaded
        documentPreview.onload = function() {
            URL.revokeObjectURL(fileURL);
        };
    } else {
        // Clear the iframe if no file is selected
        documentPreview.src = '';
    }
});
