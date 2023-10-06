from rest_framework.serializers import ModelSerializer

from education.serializer import PaymentSerializer
from users.models import User


class PublicUserSerializer(ModelSerializer):
    class Meta:
        model = User
        # exclude = ('last_name', 'password')
        fields = ('id', 'first_name', 'email', 'avatar', 'phone', 'town')


class PrivateUserSerializer(ModelSerializer):
    payments = PaymentSerializer(source='payment_set', read_only=True, many=True)

    class Meta:
        model = User
        fields = '__all__'
