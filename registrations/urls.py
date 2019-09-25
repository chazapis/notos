from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.register),
    path('register/<slug:step>', views.register, name='register'),
    path('logout/', views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]
