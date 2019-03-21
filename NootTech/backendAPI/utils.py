import base64
import uuid
import json
import os.path
from hurry.filesize import size
from pathlib import Path
from string import ascii_uppercase, ascii_lowercase
from virus_total_apis import PublicApi as VirusTotalPublicApi
from django.conf import settings
from random import choices, randint
from django.http import HttpResponseBadRequest

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
all_chars = "".join(['1234567890_', ascii_uppercase, ascii_lowercase])
vt = VirusTotalPublicApi(settings.VT_API_KEY)


def thumb_path(instance, filename):
    """
    Gets the media filepath location based on user id and generated, original filename for file THUMBNAIL image
    :param instance: - The File instance
    :param filename: - unused parameter
    :return: A string filepath for media directory of where file thumbnail will be saved
    """
    return 'Thumbnails/{0}/{1}_{2}.jpg'.format(
        instance.user.id,
        instance.generated_filename,
        instance.original_filename.split('.')[0]
    )


def file_path(instance, filename):
    """
    Gets the media filepath location based on user id and generated, original filename.
    :param instance: - The File instance
    :param filename: - unused parameter
    :return: A string filepath for media directory of where file will be saved
    """
    return 'Uploads/{0}/{1}_{2}'.format(
        instance.user.id,
        instance.generated_filename,
        instance.original_filename
    )


def scan_file(filepath):
    """
    Scans a file at filepath with virustotal API
    :param filepath: the path of the file to be scanned
    :return: a dict of scan response information
    """
    return vt.scan_file(filepath)


def get_id_gen() -> str:
    """
    :return: Generates a randomly generated upload filename which is 8 chars long
    """
    return ''.join(choices(all_chars, k=7))+str(randint(0, 99))


def get_ext(filename):
    """
    :param filename: Path to/filename (MyFile.txt)
    :return: String : file extension (.txt)
    """
    return "".join(Path(filename).suffixes).strip()


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
        ".webm", ".mp4", ".ogg", ".oggv", ".ogga", ".flac", ".wav", ".mp3"
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


def upload_authentication_failure(request, User):
    """
    Checks if the request for a file upload has all required fields (username, upload_key, etc...)
    :param request: - the request to be checked.
    :param User: - the User model
    """
    help_url = f"https://{settings.DOMAIN_NAME}/how-to"
    response_err_msg = ""

    if 'username' not in request.POST:
        response_err_msg += "- You did not provide a 'username' field\n"

    if 'upload_key' not in request.POST:
        response_err_msg += "- You did not provide an 'upload_key' field\n"

    if 'content' not in request.FILES:
        response_err_msg += "- You did not provide a 'content' file field\n"

    if 'username' in request.POST and 'upload_key' in request.POST:

        if not User.objects.filter(username=request.POST["username"], upload_key=request.POST["upload_key"]).exists():

            user = request.POST["username"]
            response_err_msg += f"- Could not authenticate user {user} with the provided upload key\n"

    if response_err_msg:
        return HttpResponseBadRequest(f"Whoops!\n{response_err_msg}Please check {help_url} for assistance.")


def get_ip(request):
    """
    Gets the IP address of a request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
