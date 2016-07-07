# -*- coding:utf-8 -*-
from exceptions import NotFound


def get_real_ip(env):
    ip = env.get('REMOTE_ADDR')
    if ip.startswith('192.168.1.') or ip == '127.0.0.1':
        ip = env.get('HTTP_X_FORWARDED_FOR')
        if isinstance(ip, (list, tuple)):
            ip = ip[-1]
        if ip:
            env['REMOTE_ADDR'] = ip
    return ip


def get_object_or_404(cls, pk):
    instance = cls.get(pk)
    if not instance:
        raise NotFound(detail='%s %s: NOT FOUND' % (cls.__name__, pk))
    return instance
