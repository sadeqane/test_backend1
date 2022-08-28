from rest_framework.permissions import DjangoModelPermissions, BasePermission


class CustomDjangoModelPermissions(DjangoModelPermissions):
    """
    It ensures that the user is authenticated, and has the appropriate
    `view`/`add`/`change`/`delete` permissions on the model.
    """
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class CustomUserPermission(BasePermission):
    """
    Allows access only to authenticated users except register user.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class CustomProductPermisstion(BasePermission):
    """
    Allows access.
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return bool(request.user and request.user.is_authenticated
                    and request.user.groups.first().name == 'seller')

    # for object level permissions
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return obj.user == request.user


class CustomBuyPermisstion(BasePermission):
    """
    Allows access.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.groups.first().name == 'buyer')

    # for object level permissions
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
