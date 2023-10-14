from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from education.models import Payment
from education.serializer import PaymentSerializer


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'payment_type')
    ordering_fields = ('purchase_date',)

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(user=self.request.user)

