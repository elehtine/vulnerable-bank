from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('bank/', include('bank.urls')),
    path('admin/', admin.site.urls),
]
