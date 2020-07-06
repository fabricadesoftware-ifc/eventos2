import magic

CONTENT_TYPE_PDF = "application/pdf"
CONTENT_TYPE_ODT = "application/vnd.oasis.opendocument.text"
CONTENT_TYPE_DOC = "application/msword"
CONTENT_TYPE_DOCX = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)
CONTENT_TYPE_TEX = "application/x-tex"
CONTENT_TYPE_ICO = "image/x-icon"
CONTENT_TYPE_JPG = "image/jpeg"
CONTENT_TYPE_PNG = "image/png"


def get_content_type(file):
    # https://stackoverflow.com/a/26419354
    if hasattr(file, "temporary_file_path"):  # pragma: no cover - no complexity
        content_type = magic.from_file(file.temporary_file_path(), mime=True)
    else:
        content_type = magic.from_buffer(file.read(), mime=True)

    # fix inconsistency in libmagic for TeX files
    if content_type == "text/x-tex":
        content_type = CONTENT_TYPE_TEX

    # it's rewind time
    if hasattr(file, "seek") and callable(
        file.seek
    ):  # pragma: no cover - no complexity
        file.seek(0)

    return content_type
