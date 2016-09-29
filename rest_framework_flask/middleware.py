# -*- coding: utf-8 -*-

from functools import wraps
from flask import request, g
from utils import get_real_ip
import urllib


def is_weixin(request):
    wx_ua = 'micromessenger'
    ua = request.environ['HTTP_USER_AGENT']
    return wx_ua in ua.lower()


def get_query_params(request):
    query_str = request.query_string.split("&")
    ret = dict()
    for key in query_str:
        ql = key.split("=")
        if len(ql) > 1:
            ret[ql[0]] = urllib.unquote(ql[1]).decode('utf8')
        elif ql:
            ret[ql[0]] = None
    return ret


def insert_args(f):
    @wraps(f)
    def _(*args, **kwargs):
        args = list(args)
        request.ip = get_real_ip(request.environ)
        request.bid = request.cookies.get('bid')
        request.user = request.environ.get('user', None)
        request.is_weixin = is_weixin(request)
        request.query_params = get_query_params(request)
        g.scheme = request.environ['wsgi.url_scheme']
        request.form
        args.insert(1, request)
        return f(*args, **kwargs)
    return _
