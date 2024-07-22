from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pyhanko.sign.signers import SimpleSigner
from pyhanko.sign import signers

def sign_pdf(input_pdf_path, output_pdf_path, cert_pem, private_key_pem):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Copy pages to writer
    for page in reader.pages:
        writer.add_page(page)

    # Initialize signer
    signer = SimpleSigner.load(cert_pem, private_key_pem)

    # Define signing options
    signing_options = signers.SigningOptions()

    # Sign the PDF
    with open(output_pdf_path, 'wb') as signed_file:
        signers.PdfSigner(
            signing_options=signing_options,
            signer=signer
        ).sign_pdf(reader, output=signed_file)
