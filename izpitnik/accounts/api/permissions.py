from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        return (
                request.user.is_superuser or
                request.user.has_perm("accounts.view_user") or
                obj.pk == request.user.pk
        )

def add_or_change_permission_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user_id = str(request.user.pk) if user_id == 'my' else user_id
        if request.method in ['POST', 'PUT', 'PATCH']:
            if not (
                    request.user.is_superuser or
                    (request.user.has_perm("accounts.change_user") and request.user.has_perm("accounts.add_user")) or
                    str(request.user.pk) == user_id
            ):
                return self.permission_denied(
                    request,
                    message="You do not have permission to perform this action."
                )
        return func(self, request, *args, **kwargs)
    return wrapper

def delete_permission_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user_id = str(request.user.pk) if user_id == 'my' else user_id
        if not  (
                request.user.is_superuser or
                request.user.has_perm("accounts.delete_user") or
                str(request.user.pk) == user_id
        ):
            return self.permission_denied(
                request,
                message="You do not have permission to perform this action."
            )
        return func(self, request, *args, **kwargs)
    return wrapper
