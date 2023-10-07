from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from education.models import Course
from education.permissions import IsOwnerOrIsSuperUser, IsStaff
from education.serializer import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_queryset(self):
        """Получение объектов Course в зависимости от пользователя"""
        queryset = super().get_queryset()

        if self.request.user.is_staff:
            return queryset.all()
        elif self.request.user:
            return queryset.filter(owner=self.request.user)
        else:
            return queryset.none()

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.owner = self.request.user
        obj.save()

    def get_permissions(self):
        if self.action in ['create']:
            # Создавать объекты могут все, кроме Staff'а
            permission_classes = [IsAuthenticated & ~IsStaff]

        elif self.action in ['update']:
            # Защита от обновления чужих объектов для обычных пользователей
            permission_classes = [IsOwnerOrIsSuperUser | IsStaff]

        elif self.action in ['destroy', 'retrieve']:
            # Защита от удаления чужих объектов для обычных пользователей
            permission_classes = [IsOwnerOrIsSuperUser]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
