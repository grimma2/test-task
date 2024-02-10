from django.contrib import admin
from django.urls import path, include
from mainapp.api import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', router.urls),
]
