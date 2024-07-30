from pyhanko.sign import signers, fields
import datetime
from pyhanko.sign.signers import cms_embedder
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

def sign_pdf(input_pdf_file, private_key):
    # Prepare the PDF for signing
    input_buf = BytesIO(input_pdf_file.read())
    writer = IncrementalPdfFileWriter(input_buf)

    # Phase 1: Setup the signature field
    cms_writer = cms_embedder.PdfCMSEmbedder().write_cms(
        field_name='Signature', writer=writer
    )
    sig_field_ref = next(cms_writer)

    # Just for verification
    assert sig_field_ref.get_object()['/T'] == 'Signature'

    # Phase 2: Create a signature object
    timestamp = datetime.now()
    sig_obj = signers.SignatureObject(timestamp=timestamp, bytes_reserved=8192)

    md_algorithm = 'sha256'
    cms_writer.send(
        cms_embedder.SigObjSetup(
            sig_placeholder=sig_obj,
            mdp_setup=cms_embedder.SigMDPSetup(
                md_algorithm=md_algorithm, certify=True,
                docmdp_perms=fields.MDPPerm.NO_CHANGES
            )
        )
    )

    # Phase 3: Prepare for signing
    prep_digest, output = cms_writer.send(
        cms_embedder.SigIOSetup(md_algorithm=md_algorithm, in_place=True)
    )

    # Phase 4: Sign the PDF
    signer = signers.SimpleSigner(
        signing_cert=None,  # If no certificate, set it to None
        private_key=private_key
    )
    cms_bytes = signer.sign(
        data_digest=prep_digest.document_digest,
        digest_algorithm=md_algorithm, timestamp=timestamp
    ).dump()
    cms_writer.send(cms_bytes)

    # The signed PDF is in `output`
    output.seek(0)
    return output