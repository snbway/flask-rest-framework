# encoding:utf-8
import re
from marshmallow import ValidationError
# from marshmallow.validate import Validator

__author__ = 'quxl'


class Phone(object):
    """Validate an Phone in China.

    :param str error: Error message to raise in case of a validation error. Can be
        interpolated with `{input}`.
    """

    PHONE_REGEX = re.compile(
        r"^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$")

    default_message = '{input} is not a valid phone.'

    def __init__(self, error=None):
        self.error = error or self.default_message

    def _format_error(self, value):
        return self.error.format(input=value)

    def __call__(self, value):
        message = self._format_error(value)

        if not value or len(value) != 11:
            raise ValidationError(message)

        if not self.PHONE_REGEX.match(value):
            raise ValidationError(message)
        return value


class Telephone(object):
    """Validate an Telephone in China.

    :param str error: Error message to raise in case of a validation error. Can be
        interpolated with `{input}`.
    """

    TELEPHONE_REGEX = re.compile(r'(([0\+]\d{2,3}-)?(0\d{2,3})-)?(\d{7,8})(-(\d{3,}))?$')

    default_message = '{input} is not a valid telephone.'

    def __init__(self, error=None):
        self.error = error or self.default_message

    def _format_error(self, value):
        return self.error.format(input=value)

    def __call__(self, value):
        message = self._format_error(value)

        if not self.TELEPHONE_REGEX.match(value):
            raise ValidationError(message)
        return value