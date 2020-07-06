import mimetypes
from secrets import token_urlsafe

from django.db import models

from eventos2.utils.files import get_content_type


def document_file_path(document, _):
    content_type = get_content_type(document.file)
    extension = mimetypes.guess_extension(content_type)
    return "documents/{}{}".format(document.public_id, extension or "")


class Document(models.Model):
    attachment_key = models.CharField(
        max_length=255,
        default=token_urlsafe,
        unique=True,
        help_text=(
            "Used to attach the document to another object. "
            "Cannot be used to retrieve the file."
        ),
    )
    public_id = models.CharField(
        max_length=255,
        default=token_urlsafe,
        unique=True,
        help_text=(
            "Used to retrieve the file itself. "
            "Should not be readable until the document is attached to another object."
        ),
    )
    file = models.FileField(upload_to=document_file_path)
    # the content type will be set by the serializer
    content_type = models.CharField(max_length=255)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # pragma: no cover - internal use
        return self.file.name

    @property
    def url(self):  # pragma: no cover - no complexity
        return self.file.url


def image_file_path(image, _):
    extension = mimetypes.guess_extension(image.file.file.content_type)
    # workaround for https://bugs.python.org/issue4963
    # it has been fixed in new python versions,
    # we should remove this sometime.
    if extension == ".jpe":  # pragma: no cover
        extension = ".jpg"
    return "images/{}{}".format(image.public_id, extension or "")


class Image(models.Model):
    attachment_key = models.CharField(
        max_length=255,
        default=token_urlsafe,
        unique=True,
        help_text=(
            "Used to attach the image to another object. "
            "Cannot be used to retrieve the image file."
        ),
    )
    public_id = models.CharField(
        max_length=255,
        default=token_urlsafe,
        unique=True,
        help_text=(
            "Used to retrieve the image itself. "
            "Should not be readable until the image is attached to another object."
        ),
    )
    file = models.ImageField(upload_to=image_file_path)
    description = models.CharField(max_length=255, blank=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # pragma: no cover - internal use
        return self.description

    @property
    def url(self):  # pragma: no cover - no complexity
        return self.file.url
