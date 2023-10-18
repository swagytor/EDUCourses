import stripe
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
    payment_info = serializers.SerializerMethodField()

    def get_payment_info(self, instance):
        if instance.session_id:
            intent = stripe.checkout.Session.retrieve(instance.session_id)

            return intent
        return None

    class Meta:
        model = Payment
        fields = ['user', 'purchase_date', 'course', 'payment_type', 'payment_info']


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'
