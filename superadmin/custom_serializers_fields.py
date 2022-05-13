from rest_framework import serializers
from drf_extra_fields.fields import Base64FileField

from django.core.exceptions import ValidationError
import imghdr
import PyPDF2
import io
# from rest_framework.fields import WritableField

# ===================================================================
''' Custom Serializer Method field to add read write support to SerializerMethodField '''
# ===================================================================


class ReadWriteSerializerMethodField(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        super(serializers.SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {self.field_name: data}
# ===================================================================


class CustomBase64FileField(Base64FileField):
    ALLOWED_TYPES = ['pdf', 'png', 'jpg', 'webp']

    def get_file_extension(self, filename, decoded_file):
        # Check if file is PDF
        try:
            PyPDF2.PdfFileReader(io.BytesIO(decoded_file))
        except PyPDF2.utils.PdfReadError as e:
            print(e)
        else:
            return 'pdf'

        # Check if file is Image
        try:
            from PIL import Image
        except ImportError:
            raise ImportError("Pillow is not installed.")
        extension = imghdr.what(filename, decoded_file)
        print(extension)
        # Try with PIL as fallback if format not detected due
        # to bug in imghdr https://bugs.python.org/issue16512
        if extension is None:
            try:
                image = Image.open(io.BytesIO(decoded_file))
            except (OSError, IOError):
                raise ValidationError(self.INVALID_FILE_MESSAGE)

            extension = image.format.lower()

        extension = "jpg" if extension == "jpeg" else extension
        return extension

        raise ValidationError(self.INVALID_FILE_MESSAGE)


