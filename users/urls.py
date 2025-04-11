from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from users.apps import UsersConfig
from users.views import UserViewSet


router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

app_name = UsersConfig.name

urlpatterns = [
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + router.urls
