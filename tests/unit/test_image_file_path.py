from django.core.files.uploadedfile import SimpleUploadedFile

from eventos2.media.models import Image, image_file_path


def make_image(*, content_type):
    return Image(
        file=SimpleUploadedFile(
            name="file_name", content=b"file_content", content_type=content_type
        )
    )


def test_image_file_path_jpg():
    img = make_image(content_type="image/jpeg")
    assert image_file_path(img, None).endswith(".jpg")


def test_image_file_path_png():
    img = make_image(content_type="image/png")
    assert image_file_path(img, None).endswith(".png")
