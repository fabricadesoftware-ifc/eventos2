import base64

from django.core.files.uploadedfile import SimpleUploadedFile

from eventos2.images.serializers import ImageUploadSerializer


def test_imageuploadserializer_valid():
    # DADO um arquivo JPEG
    jpg_content = base64.b64decode(
        "/9j/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDR"
        "ENDg8QEBEQCgwSExIQEw8QEBD/yQALCAABAAEBAREA/8wABgAQEAX/2gAIAQEAAD8A0s8g"
        "/9k="
    )
    file = SimpleUploadedFile("image.jpeg", jpg_content)

    # QUANDO passar pelo serializer
    serializer = ImageUploadSerializer(data=dict(file=file))

    # ENTÃO será válido
    assert serializer.is_valid()


def test_imageuploadserializer_invalid():
    # DADO um arquivo PDF
    pdf_content = base64.b64decode(
        "JVBERi0xLgoxIDAgb2JqPDwvUGFnZXMgMiAwIFI+PmVuZG9iagoyIDAgb2JqPDwvS2lkc1"
        "szIDAgUl0vQ291bnQgMT4+ZW5kb2JqCjMgMCBvYmo8PC9QYXJlbnQgMiAwIFI+PmVuZG9i"
        "agp0cmFpbGVyIDw8L1Jvb3QgMSAwIFI+Pg=="
    )
    file = SimpleUploadedFile("file.pdf", pdf_content)

    # QUANDO passar pelo serializer
    serializer = ImageUploadSerializer(data=dict(file=file))

    # ENTÃO não será válido (não é uma imagem)
    assert not serializer.is_valid()


def test_imageuploadserializer_blocked():
    # DADO um arquivo GIF
    ico_content = base64.b64decode(
        "AAABAAEAAQEAAAEAGAAwAAAAFgAAACgAAAABAAAAAgAAAAEAGAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAP8AAAAAAA=="
    )
    file = SimpleUploadedFile("file.ico", ico_content)

    # QUANDO passar pelo serializer
    serializer = ImageUploadSerializer(data=dict(file=file))

    # ENTÃO não será válido (é imagem, mas não é JPEG ou PNG)
    assert not serializer.is_valid()
