from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        """Проверка на принадлежность пользователя к менеджерам"""
        return not request.user.is_superuser and request.user.is_staff


class IsOwnerOrIsSuperUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        """Проверка на принадлежность пользователя к админу или к владельцу объекта"""
        if request.user.is_superuser and request.user.is_staff:
            return True
        return request.user == obj.owner


class IsCourseOwner(BasePermission):
    """Проверка на принадлежность пользователя к владельцу курса"""
    def has_object_permission(self, request, view, obj):
        course = obj.course
        return course.owner == request.user
