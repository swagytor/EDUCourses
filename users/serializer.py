from rest_framework.serializers import ModelSerializer

from education.serializer import PaymentSerializer
from users.models import User


class UserSerializer(ModelSerializer):
    payments = PaymentSerializer(source='payment_set', read_only=True, many=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'town', 'avatar', 'payments',)
