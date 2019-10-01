from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.register),
    path('register/<slug:step>', views.register, name='register'),
    path('logout/', views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
