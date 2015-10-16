# -*- coding:utf-8 -*-

from rest_framework.views import APIView
from schemas import HelloSchema
from permissions import ExamplesPermission


class HelloView(APIView):
    permission_classes = (ExamplesPermission, )
    schema_class = {'default': HelloSchema }

    def get(self, request, *args, **kwargs):
        return dict(msg='Hello')
