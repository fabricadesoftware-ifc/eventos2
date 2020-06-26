import mimetypes
from secrets import token_urlsafe

from django.db import models


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
