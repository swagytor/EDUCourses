from rest_framework import serializers
from education.models import Course, Lesson, Payment, Subscribe
from education.validators import URLValidator


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(max_length=150, validators=[URLValidator()])

    class Meta:
        model = Lesson
        exclude = ('id', 'preview')


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', read_only=True, many=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, course):
        return course.lesson_set.count()

    def get_is_subscribed(self, course):
        user = self.context['request'].user
        return course.subscribe_set.filter(user=user).exists()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'
