from django.urls import path
from rest_framework.routers import DefaultRouter

from education.apps import EducationConfig
from education.views.course import CourseViewSet
from education.views.lesson import LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView
from education.views.payment import PaymentListAPIView, create_payment, PaymentRetrieveAPIView
from education.views.subscribe import course_subscription

app_name = EducationConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
                  path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
                  path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
                  path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
                  path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
                  path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),

                  path('payment/list/', PaymentListAPIView.as_view(), name='payment-list'),
                  path('payment/details/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment-get'),

                  path('course/pay/<int:course_pk>/', create_payment, name='course-pay'),
                  path('course_subscription/<int:pk>/', course_subscription, name='course-subscription'),
              ] + router.urls
