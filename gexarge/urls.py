from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('db/', admin.site.urls),
   path('', include('web.urls')),
]
