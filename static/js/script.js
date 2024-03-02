
function previewPDF() {
  const fileInput = document.getElementById('pdf-upload');
  const pdfPreview = document.getElementById('pdf-preview');

  if (fileInput.files.length === 0) {
      alert("Please select a PDF file to upload.");
      return;
  }

  const file = fileInput.files[0];
  if(file.type !== "application/pdf") {
      alert("Please select a PDF file.");
      return;
  }

  // Use FileReader to read file
  const fileReader = new FileReader();

  fileReader.onload = function() {
      pdfPreview.src = fileReader.result;
      pdfPreview.hidden = false;
  };

  fileReader.readAsDataURL(file);
}

