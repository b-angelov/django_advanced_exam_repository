from rest_framework import permissions


class IsAuthorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
                request.user.is_superuser or
                request.user.has_perm("articles.change_article") or
                obj.author.pk == request.user.pk
        )

class IsAuthorOnAllMethodsPermission(IsAuthorPermission):

    def has_object_permission(self, request, view, obj):
        return (
                request.user.is_superuser or
                request.user.has_perm("articles.change_article") or
                obj.author.pk == request.user.pk
        )