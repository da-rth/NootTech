from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.contrib.auth import get_user_model
import MailChecker
import string
import re

User = get_user_model()
m = MailChecker.MailChecker()

with open('backendAPI/blacklists/reserved_subdomains.txt') as f:
    reserved_subdomains = set(f.read().strip().split('\n'))

with open('backendAPI/blacklists/disallowed_profanity.txt') as f:
    profanity = set(f.read().strip().split('\n'))


leet_speak = (('a', '4'), ('e', '3'), ('i', '1'), ('o', '0'), ('t', '7'), ('g', '9'))


class NumberValidator(object):
    '''
    Checks if a password contains a numerical value
    '''
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                _(mark_safe("The password must contain at least <strong>one numerical character</strong> (0-9)")),
                code='password_no_number',)

    def get_help_text(self):
        return ""


class UppercaseValidator(object):
    '''
    Checks if a password contains an uppercase letter
    '''
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _(mark_safe("The password must contain at least <strong>one uppercase letter</strong> (A-Z).")),
                code='password_no_upper',)

    def get_help_text(self):
        return ""


class LowercaseValidator(object):
    '''
    Checks if a password contains a lowercase letter
    '''
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _(mark_safe("The password must contain at least <strong>one lowercase letter</strong> (a-z).")),
                code='password_no_lower',)

    def get_help_text(self):
        return ""


def validate_email(email):
    '''
    Checks if an email is disposable or incorrectly formatted.
    '''
    if '@' in email and '.' in email:

        if not m.is_valid(email):
            name, domain = email.split('@')
            raise ValidationError(_(mark_safe("Sorry, we don't allow disposable email addresses. "
                                    "The domain <strong>{}</strong> has been blacklisted.".format(domain))))
        emailset = Q(email__icontains=email)
        emailres = User.objects.filter(emailset)
        if emailres:
            raise ValidationError(_(mark_safe("This email address has already been taken.")))


def validate_username(username):
    '''
    Checks if a username is reserved, too short, contains cursewords etc...
    '''
    usernameset = Q(username__icontains=username) | Q(email__icontains=username)
    usernameres = User.objects.filter(usernameset)
    if usernameres:
        raise ValidationError(_(mark_safe("This username has already been taken.")))

    if not re.match("^[A-Za-z0-9_-]*$", username):
        raise ValidationError(_(mark_safe("A username must <strong>only</strong> contain letters, numbers, "
                                          "underscores and dashes.")))

    if username.lower() in reserved_subdomains or (username.lower().startswith('www') and re.findall('\d', username)):
        raise ValidationError(_(mark_safe("The username <strong>{}</strong> is <strong>disallowed</strong>. "
                                          "Try something normal.".format(username))))

    # Underscore and hyphen strip
    stripped_username = username.replace('-', '').replace('_', '')

    # l33t sp33k Conversion
    for norm, leet in leet_speak:
        stripped_username = stripped_username.replace(leet, norm)

    if any(word in stripped_username for word in profanity):
        raise ValidationError(_(mark_safe("The username <strong>{}</strong> contains profanity and cannot be used.".format(username))))


def validate_colour(colour):
    '''
    Checks if the provided colour is in HEX format.
    '''
    if len(colour) != 7 or not all(c in string.hexdigits for c in colour[1:]):
        raise ValidationError(_(mark_safe("Your chosen colour must in a <strong>6 digit hex-code</strong> format "
                                          "(e.g. #FFFFFF).")))
