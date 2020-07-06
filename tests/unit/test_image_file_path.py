from django.core.files.uploadedfile import SimpleUploadedFile

from eventos2.media.models import Image, image_file_path
from eventos2.utils.files import CONTENT_TYPE_JPG, CONTENT_TYPE_PNG


def make_image(*, content_type):
    return Image(
        file=SimpleUploadedFile(
            name="file_name", content=b"file_content", content_type=content_type
        )
    )


def test_image_file_path_jpg():
    img = make_image(content_type=CONTENT_TYPE_JPG)
    assert image_file_path(img, None).endswith(".jpg")


def test_image_file_path_png():
    img = make_image(content_type=CONTENT_TYPE_PNG)
    assert image_file_path(img, None).endswith(".png")
