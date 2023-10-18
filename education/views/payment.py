from pprint import pprint

import stripe
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from education.models import Payment, Course
from education.serializer import PaymentSerializer
from education.views.services import get_checkout_session


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'payment_type')
    ordering_fields = ('purchase_date',)

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request, course_pk):
    try:
        course = Course.objects.get(pk=course_pk)

        if course:
            checkout_session = get_checkout_session(request, course)

            data = {
                'user': request.user.pk,
                'course': course.pk,
                'session_id': checkout_session.get('id'),
                'session_url': checkout_session.get('url'),
                'payment_intent': checkout_session.get('payment_intent')
            }

            serializer = PaymentSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({"session_url": checkout_session.get('url')}, status=status.HTTP_200_OK)

            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Course.DoesNotExist:
        return Response({"error": "Курс не найден!"}, status=status.HTTP_404_NOT_FOUND)


class PaymentRetrieveAPIView(RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
