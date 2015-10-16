# encoding: utf-8
from . import api_setting
import exceptions


class BaseVersioning(object):
    default_version = api_setting.DEFAULT_VERSION
    allowed_versions = api_setting.ALLOWED_VERSION
    version_param = api_setting.VERSION_PARAM

    def determine_version(self, request, *args, **kwargs):
        msg = '{cls}.determin_version() must be iimplemented.'
        raise NotImplementedError(msg.format(
            cls=self.__class__.__name__
        ))

    def reverse(self, *args, **kwargs):
        pass

    def is_allowed_version(self, version):
        if not self.allowed_versions:
            return True
        return (version == self.default_version) or (version in self.allowed_versions)


class QueryParameterVersioning(BaseVersioning):
    invalid_version_message = 'Invalid version in URL path.'

    def determine_version(self, request, *args, **kwargs):
        version = request.query_params.get(self.version_param, self.default_version)
        if not self.is_allowed_version(version):
            raise exceptions.NotFound(self.invalid_version_message)
        return version

    def reverse(self, viewname, args=None, kwargs=None, request=None, format=None, **extra):
        if request.version is not None:
            kwargs = {} if (kwargs is None) else kwargs
            kwargs[self.version_param] = request.version

        return super(QueryParameterVersioning, self).reverse(
            viewname, args, kwargs, request, format, **extra
        )
