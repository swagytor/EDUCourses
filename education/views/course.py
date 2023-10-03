from rest_framework import viewsets

from education.models import Course
from education.serializer import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

