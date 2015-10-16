# -*- coding:utf-8 -*-
from rest_framework.schemas import fields
from rest_framework.schemas import Schema


class HelloSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
