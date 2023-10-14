from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from education.models import Subscribe, Course
from education.serializer import SubscribeSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_subscription(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({'error': 'Такого курса не существует!'}, status=status.HTTP_404_NOT_FOUND)
    else:
        if Subscribe.objects.filter(user=request.user, course=course).exists():
            Subscribe.objects.filter(user=request.user, course=course).delete()
            return Response({'message': 'Подписка на курс отменена!'}, status=status.HTTP_200_OK)

        data = {'user': request.user.id, 'course': pk}
        serializer = SubscribeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Вы подписались на курс!'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
