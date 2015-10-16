# -*- coding:utf-8 -*-


def get_real_ip(env):
    ip = env.get('REMOTE_ADDR')
    if ip.startswith('192.168.1.') or ip == '127.0.0.1':
        ip = env.get('HTTP_X_FORWARDED_FOR')
        if isinstance(ip, (list, tuple)):
            ip = ip[-1]
        if ip:
            env['REMOTE_ADDR'] = ip
    return ip