from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from users.apps import UsersConfig
from users.views import UserUpdateAPIView, UserListAPIView, UserRetrieveAPIView

app_name = UsersConfig.name
#
# router = DefaultRouter()
# router.register(r'', UserReadOnlyViewSet, basename='users')


urlpatterns = [
    path('', UserListAPIView.as_view(), name='user-list'),
    path('details/<int:pk>/', UserRetrieveAPIView.as_view(), name='user-get'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),

    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
