from rest_framework.generics import UpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.permissions import IsOwnAccount
from users.serializer import PrivateUserSerializer, PublicUserSerializer


# Create your views here.
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return PrivateUserSerializer
        return PublicUserSerializer


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer
    permission_classes = [IsOwnAccount]

