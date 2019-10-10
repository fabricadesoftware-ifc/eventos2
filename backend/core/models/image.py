import mimetypes
from secrets import token_urlsafe

from django.db import models


def image_file_path(instance, filename):
    extension = mimetypes.guess_extension(instance.file.file.content_type)
    if extension == ".jpe":
        extension = ".jpeg"
    return "images/{}{}".format(instance.public_id, extension)


class Image(models.Model):
    public_id = models.CharField(
        max_length=255,
        default=token_urlsafe,
        unique=True,
        help_text="User-facing identifier",
    )
    file = models.ImageField(upload_to=image_file_path)
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
