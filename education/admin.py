from django.contrib import admin

from education.models import Lesson, Course, Payment


# Register your models here.
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'course_id',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'price')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'purchase_date', 'payment_type',)
    ordering = ('course',)
