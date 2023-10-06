from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from education.models import Lesson
from education.permissions import IsOwnerOrIsSuperUser, IsStaff, IsCourseOwner
from education.serializer import LessonSerializer


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & ~IsStaff]


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_queryset(self):
        """Получение объектов Lesson в зависимости от пользователя"""
        queryset = super().get_queryset()

        if self.request.user:
            return queryset.filter(owner=self.request.user)

        elif self.request.user.is_staff:
            return queryset.all()

        else:
            return queryset.none()

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.owner = self.request.user
        obj.save()


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrIsSuperUser]


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsStaff | IsCourseOwner | IsOwnerOrIsSuperUser]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrIsSuperUser]
