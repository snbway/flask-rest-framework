# encoding:utf-8

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class BasePermission(object):
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


# class permission

class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return True if request.user else False


# object permission
class IsOwner(BasePermission):
    """
    Allow access only object owner.
    """

    def has_object_permission(self, request, view, obj):
        if not request or not request.user or not obj:
            return False
        owner_id = 0
        if hasattr(obj, 'user_id'):
            owner_id = getattr(obj, 'user_id')
        elif hasattr(obj, 'creator_id'):
            owner_id = getattr(obj, 'creator_id')
        elif hasattr(obj, 'author_id'):
            owner_id = getattr(obj, 'author_id')
        return str(owner_id) == str(request.user.id)
