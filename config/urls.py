from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('habits.urls', namespace='habits')),
    path('', include('users.urls', namespace='users')),
]
