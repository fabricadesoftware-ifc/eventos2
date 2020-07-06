from django.core.files.uploadedfile import SimpleUploadedFile

from eventos2.media.models import Document, document_file_path
from eventos2.utils.files import CONTENT_TYPE_PDF, CONTENT_TYPE_TEX


def make_document():
    return Document(file=SimpleUploadedFile(name="file_name", content=b"file_content"))


def test_document_file_path_pdf(monkeypatch):
    monkeypatch.setattr(
        "eventos2.media.models.get_content_type", lambda x: CONTENT_TYPE_PDF
    )
    doc = make_document()
    assert document_file_path(doc, None).endswith(".pdf")


def test_document_file_path_tex(monkeypatch):
    monkeypatch.setattr(
        "eventos2.media.models.get_content_type", lambda x: CONTENT_TYPE_TEX
    )
    doc = make_document()
    assert document_file_path(doc, None).endswith(".tex")
