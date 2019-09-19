from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]
