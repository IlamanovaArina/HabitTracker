from django.urls import path
from rest_framework.routers import DefaultRouter
from habits.apps import HabitsConfig
from habits.views import HabitsViewSet, AwardViewSet

router = DefaultRouter()
router.register(r'habit', HabitsViewSet, basename='habit')
router.register(r'award', AwardViewSet, basename='award')

app_name = HabitsConfig.name

urlpatterns = [
    # path('habits/', HabitsViewSet.as_view(), name='')
] + router.urls
