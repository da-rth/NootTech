import base64
import uuid
import json
import os.path
from hurry.filesize import size
from pathlib import Path
from string import ascii_uppercase, ascii_lowercase
from django.utils.http import int_to_base36

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
all_chars = "".join(['1234567890-_=$', ascii_uppercase, ascii_lowercase])


def get_id_gen() -> str:
    """
    :return: Generates a randomly generated upload filename which is 8 chars long
    """
    return int_to_base36(uuid.uuid4().int)[:8]


def get_ext(filename):
    """
    :param filename: Path to/filename (MyFile.txt)
    :return: String : file extension (.txt)
    """
    return "".join(Path(filename).suffixes)


def get_upload_key():
    """
    Generates a randomised upload key for a user.
    This key is used for authenticating remote uploads (cURL, ShareX) instead of exposing user password.
    :return: String - randomly generate string of 24 characters
    """
    key = base64.b64encode(uuid.uuid4().bytes).decode("utf-8")[:-2]
    return key


def get_client_ip(request):
    """
    :param request: - Object containing POST Request Information
    :return: String : the IP address of the POST request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_websafe(ext):
    """
    :param ext: - a file extension (str)
    :return: - Boolean : if file extension is marked as web-browser compatible
    """
    web_safe = [
        ".png", ".jpg", ".jpeg", ".gif", ".svg", ".bmp", ".ico",
        ".webm", ".mp4", ".ogg", ".oggv", ".ogga", ".flac", ".wav"
    ]
    if ext.lower() in web_safe:
        return True
    else:
        return False


def get_filesize_str(size_bytes):
    """
    :param size_bytes: - size of a file in bytes
    :return: - String: filesize converted to KB, MB, GB...
    """
    return size(size_bytes)


def get_fontawesome(mimetype, ext):
    """
    :param mimetype: - The estimated mime-type of a file (e.g. audio/mp3)
    :param ext: - The extension of a file (.mp3)
    :return: String : a string representing the class-name of an icon for FontAwesome's ICON set
    """
    mimes = json.load(open(os.path.join(DIR, 'backendAPI/utils/fa_mimetypes.json')))
    if ext in mimes["codeTypes"]:
        return "fas fa-code"
    elif ext in mimes["fontTypes"]:
        return "fas fa-font"
    elif ext in mimes["otherTypes"]:
        return mimes["otherTypes"][ext]
    else:
        mimetype = mimetype.split('/')
        if mimetype[0] in mimes:
            print(mimetype[0])
            if isinstance(mimes[mimetype[0]], str):
                return mimes[mimetype[0]]
            if mimetype[1] in mimes[mimetype[0]]:
                return mimes[mimetype[0]][mimetype[1]]
        icon = "fas fa-file"
    return icon


def get_syntax_highlighting(ext, mimetype):
    """
    :param mimetype: - The estimated mime-type of a file (e.g. text/plain)
    :param ext: - The extension of a file (.py)
    :return: String : the highlighting language used for highlightjs
    """
    ext = ext.split(".")[-1]
    hljs = json.load(open(os.path.join(DIR, 'backendAPI/utils/hljs.json')))
    ftype = mimetype.split("/")[1].lower()

    if ext.lower() in hljs:
        return hljs[ext.lower()]
    elif ftype in hljs:
        return hljs[ftype]
    else:
        return ""


def get_chars_lines(filename):
    """
    :param filename: - The path to a text-file
    :return: Tuple : number of characters and lines in the text file
    """
    with open(filename) as f:
        fr = f.readlines()
        chars = sum([len(i) - 1 for i in fr])
        lines = len(fr)
    return chars, lines
