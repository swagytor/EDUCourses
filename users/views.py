from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet

from users.models import User
from users.serializer import UserSerializer


# Create your views here.
class UserViewSet(ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
