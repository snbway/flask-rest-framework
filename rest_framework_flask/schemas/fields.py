# encoding:utf-8

from marshmallow.fields import ValidatedField
from marshmallow.fields import *
from ..validator import Phone as Phone_validate, Telephone as Telephone_validate


class Phone(ValidatedField, String):

    def __init__(self, *args, **kwargs):
        String.__init__(self, *args, **kwargs)
        # Insert validation into self.validators so that multiple errors can be
        # stored.
        self.validators.insert(0, Phone_validate(error=getattr(self, 'error')))

    def _validated(self, value):
        if value is None:
            return None
        return Phone_validate(
            error=getattr(self, 'error')
            )(value)


class Telephone(ValidatedField, String):

    def __init__(self, *args, **kwargs):
        String.__init__(self, *args, **kwargs)
        # Insert validation into self.validators so that multiple errors can be
        # stored.
        self.validators.insert(0, Telephone_validate(error=getattr(self, 'error')))

    def _validated(self, value):
        if value is None:
            return None
        return Telephone_validate(
            error=getattr(self, 'error')
            )(value)