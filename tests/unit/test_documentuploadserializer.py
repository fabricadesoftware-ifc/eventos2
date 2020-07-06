from django.core.files.uploadedfile import SimpleUploadedFile

from eventos2.media.serializers import DocumentUploadSerializer
from eventos2.utils.files import CONTENT_TYPE_JPG, CONTENT_TYPE_PDF


def test_documentuploadserializer_valid(monkeypatch):
    # DADO um arquivo detectado como PDF
    file = SimpleUploadedFile("file_name", b"file_content")
    monkeypatch.setattr(
        "eventos2.media.serializers.get_content_type", lambda x: CONTENT_TYPE_PDF
    )

    # QUANDO passar pelo serializer
    serializer = DocumentUploadSerializer(data=dict(file=file))

    # ENTÃO será válido
    assert serializer.is_valid()
    # E ENTÃO o content type detectado será salvo
    assert serializer.validated_data["content_type"] == CONTENT_TYPE_PDF


def test_documentuploadserializer_invalid(monkeypatch):
    # DADO um arquivo detectado como JPEG
    file = SimpleUploadedFile("file_name", b"file_content")
    monkeypatch.setattr(
        "eventos2.media.serializers.get_content_type", lambda x: CONTENT_TYPE_JPG
    )

    # QUANDO passar pelo serializer
    serializer = DocumentUploadSerializer(data=dict(file=file))

    # ENTÃO não será válido (não é um documento)
    assert not serializer.is_valid()
