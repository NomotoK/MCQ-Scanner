import fitz  # Import PyMuPDF

def convert_pdf_to_jpg(pdf_path, output_folder='images/pdf_converted', dpi=300):
    doc = fitz.open(pdf_path)  # Open the PDF file
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # Load the current page
        pix = page.get_pixmap(dpi=dpi)  # Render page to an image
        output_path = f"{output_folder}/page_{page_num + 1}.jpg"
        pix.save(output_path)  # Save the image as a JPG

# Example usage
pdf_path = 'pdf/test.pdf'
convert_pdf_to_jpg(pdf_path)