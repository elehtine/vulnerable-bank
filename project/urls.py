from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view(next_page='/')),
    path('', include('bank.urls')),
]
