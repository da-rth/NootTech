from django.utils import deconstruct
from django.template.defaultfilters import filesizeformat

@deconstruct
class FileValidator(object):
    error_message = {
        'max_size':("File Size grater than highest allowed size of %(max_size)s."
                    "File Size %(size)"),
        'min_size': ("File size less than minimun allowed size of %(min_size)s. "
                  "Your file size is %(size)s."),
    }