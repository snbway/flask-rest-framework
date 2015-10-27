# encoding:utf-8
from marshmallow import Schema as MSchema


class Schema(MSchema):

    def __init__(self, *args, **kwargs):
        self.method = kwargs.pop('method', None)
        self.instance = None
        super(Schema, self).__init__(*args, **kwargs)

    def load(self, data, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        self.instance = instance
        if 'PUT' == self.method:
            valid_fields = list(set(data).intersection(set(self.fields.keys())))
            self._clean_none_fields(valid_fields)
        data = self.translate_empty_2_none(data)
        data, error = super(Schema, self).load(data, *args, **kwargs)
        return self.translate_none_2_empty(data), error

    def translate_empty_2_none(self, data):
        data_dict = data.to_dict()
        for key in data_dict:
            if data_dict[key] == "" and self.fields[key].allow_none:
                data_dict[key] = None
        return data_dict

    def translate_none_2_empty(self, data):
        for key in data:
            if data[key] is None and self.fields[key].allow_none:
                data[key] = ""
        return data

    def _clean_none_fields(self, valid_fields):
        clean_fields = list(set(self.fields.keys()).difference(set(valid_fields)))
        for f in clean_fields:
            del self.fields[f]
