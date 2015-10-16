# -*- coding: utf-8 -*-


def permissions(permission_classes):
    def decorator(func):
        func.permission_classes = permission_classes
        return func
    return decorator

