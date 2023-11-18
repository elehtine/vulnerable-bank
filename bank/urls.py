from django.urls import path

from . import views

app_name = 'bank'
urlpatterns = [
    path('<username>/', views.account, name='account'),
]
