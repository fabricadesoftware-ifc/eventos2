import base64

from django.core.files.uploadedfile import SimpleUploadedFile

from eventos2.utils.files import (
    CONTENT_TYPE_JPG,
    CONTENT_TYPE_PDF,
    CONTENT_TYPE_TEX,
    get_content_type,
)


def test_documentuploadserializer_valid_pdf():
    # DADO um arquivo PDF
    pdf_content = base64.b64decode(
        "JVBERi0xLgoxIDAgb2JqPDwvUGFnZXMgMiAwIFI+PmVuZG9iagoyIDAgb2JqPDwvS2lkc1"
        "szIDAgUl0vQ291bnQgMT4+ZW5kb2JqCjMgMCBvYmo8PC9QYXJlbnQgMiAwIFI+PmVuZG9i"
        "agp0cmFpbGVyIDw8L1Jvb3QgMSAwIFI+Pg=="
    )
    file = SimpleUploadedFile("file.pdf", pdf_content)

    # ENTÃO o content type deve corresponder
    assert get_content_type(file) == CONTENT_TYPE_PDF


def test_documentuploadserializer_valid_tex():
    # DADO um arquivo TeX
    tex_content = base64.b64decode(
        "XGRvY3VtZW50Y2xhc3N7YXJ0aWNsZX0KXGJlZ2lue2RvY3VtZW50fQpUaGlzIGlzIGEgc2"
        "FtcGxlIGZpbGUgaW4gdGhlIHRleHQgZm9ybWF0dGVyIFxMYVRlWC4KXGVuZHtkb2N1bWVu"
        "dH0K"
    )
    file = SimpleUploadedFile("file.tex", tex_content)

    # ENTÃO o content type deve corresponder
    assert get_content_type(file) == CONTENT_TYPE_TEX


def test_documentuploadserializer_invalid():
    # DADO um arquivo JPEG
    jpg_content = base64.b64decode(
        "/9j/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDR"
        "ENDg8QEBEQCgwSExIQEw8QEBD/yQALCAABAAEBAREA/8wABgAQEAX/2gAIAQEAAD8A0s8g"
        "/9k="
    )
    file = SimpleUploadedFile("file.jpeg", jpg_content)

    # ENTÃO o content type deve corresponder
    assert get_content_type(file) == CONTENT_TYPE_JPG
