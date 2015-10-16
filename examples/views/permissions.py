# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission
import random


class ExamplesPermission(BasePermission):

    def has_permission(self, request, view):
        return random.choice([True, False])
