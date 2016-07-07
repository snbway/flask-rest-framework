# encoding=utf-8
from flask import Response
from flask.ext.restful import Resource

import exceptions
from exceptions import APIException, NotAuthenticated, AuthenticationFailed
from middleware import insert_args
import status
from utils import get_object_or_404
from versioning import QueryParameterVersioning
import api_setting


class APIView(Resource):

    permission_classes = ()
    schema_class = {}
    model = None
    versioning_class = QueryParameterVersioning
    fields = ()

    lookup_key = 'pk'
    allow_method = ('GET', 'PUT', 'DELETE', 'POST')

    def get_schema_class(self, version):
        return self.schema_class.get(version, self.schema_class.get("default"))

    def get_schema(self, **kwargs):

        assert len(self.schema_class) > 0, (
            '{cls}.schema_class can not empty!'.format(
                cls=self.__class__.__name__
            )
        )

        assert 'default' in self.schema_class, (
            '{cls}.schema_class must has the key \'default\'!'.format(
                cls=self.__class__.__name__
            )
        )
        schema = self.get_schema_class(self.request.version)
        only = []
        if 'fields' in self.request.args:
            only = self.request.args['fields'].split(',')
            only.extend(kwargs.get('only', []))
            only = list(set(only).intersection(set(schema().fields.keys())))

        if self.fields:
            only.extend(self.fields)
            only = list(set(only).intersection(set(schema().fields.keys())))
        if only:
            kwargs['only'] = only
        kwargs['method'] = self.request.method
        return schema(**kwargs)

    def permission_denied(self, request, message=None):
        """
        If request is not permitted, determine what kind of exception to raise.
        """
        if not request.user:
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(detail=message)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """

        class_permissions = [permission_class for permission_class in self.permission_classes]
        method_permissions = []
        method = getattr(self, self.request.method.lower(), None)
        if hasattr(method, 'permission_classes'):
            method_permissions = [permission_class for permission_class in getattr(method, 'permission_classes')]
        class_permissions.extend(method_permissions)
        return [permission() for permission in set(class_permissions)]

    def check_object_permissions(self, request, obj):
        """
        Check if the request should be permitted for a given object.
        Raises an appropriate exception if the request is not permitted.
        """

        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )

    def check_permissions(self, request):
        """
        Check if the request should be permitted.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )

    def handle_exception(self, exc):
        if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
            exc.status_code = status.HTTP_401_UNAUTHORIZED
        return Response(response=exc.default_detail, status=exc.status_code)

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        self.check_permissions(request)

        # Determine the API version, if version is in use.
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.version_schema = version, scheme

    def determine_version(self, request, *args, **kwargs):
        """
        If versioning is being used, then determine any API version from
        incomming request. Returns a two-tuple of(version, version_scheme)
        """
        if self.versioning_class is None:
            return (None, None)
        scheme = self.versioning_class()
        return (scheme.determine_version(request, *args, **kwargs), scheme)

    @insert_args
    def dispatch_request(self, *args, **kwargs):
        self.kwargs = kwargs
        self.args = args
        self.request = args[0]

        try:
            if self.request.method.upper() not in self.allow_method:
                raise exceptions.MethodNotAllowed()
            request = args[0]
            self.initial(request, *args, **kwargs)
            response = super(APIView, self).dispatch_request(*args, **kwargs)
        except APIException as exc:
            response = self.handle_exception(exc)
        return response


class ListAPIView(APIView):

    def __init__(self, *args, **kwargs):
        self.max_page_size = 100
        super(ListAPIView, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.parse_page_args()
        queryset, total = self.get_query_set()
        # sorted by fields, such as id,create_time,etc....
        if len(queryset) > 0:
            sorted_by = [key.strip() for key in request.args.get('sorted_by', '').split(',') if key.strip() != ""]
            queryset = sorted(queryset, key=lambda x: [getattr(x, key) for key in sorted_by if hasattr(queryset[0], key)])
        # paginate queryset where result > self.page_size
        schema = self.get_schema(many=True)
        ret = schema.dump(queryset)
        if total is not None:
            result = self.get_paginated_response(ret.data, total)
        else:
            result = ret.data
        return result

    def get_query_set(self):
        raise NotImplementedError('subclasses of {cls} must provide a get_query_set() method'\
                                  .format(cls=self.__class__.__name__))

    def parse_page_args(self):
        page = int(self.request.args.get('page', 1))
        page_size = int(self.request.args.get('page_size', 10))
        self.page = page if page > 0 else 1
        max_page = self.max_page_size or 100
        self.page_size = page_size if page_size in range(1, max_page) else api_setting.PAGE_SIZE

    def get_paginated_response(self, queryset, total):
        ret = dict(page=self.page, items=queryset, total=total)
        return ret

    def paginate_queryset(self, total):
        return total > self.page_size


class DetailAPI(APIView):

    def get_object(self):
        schema = self.get_schema()
        return get_object_or_404(schema.Meta.model, self.kwargs.get(self.lookup_key))

    def get(self, request, *args, **kwargs):
        inst = self.get_object()
        schema = self.get_schema()
        self.check_object_permissions(request, inst)
        return schema.dum(inst).data

    def put(self, request, *args, **kwargs):
        inst = self.get_object()
        schema = self.get_schema()
        self.check_object_permissions(request, inst)
        data, error = schema.load(request.form)
        if error:
            return error, 400
        inst = schema.update(instance=inst, **data)
        return schema.dump(inst).data

    def delete(self, request, *args, **kwargs):
        inst = self.get_object()
        self.check_object_permissions(request, inst)
        if inst.delete():
            return '', 204
        return '删除失败', 500