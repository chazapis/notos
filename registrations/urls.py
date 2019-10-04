from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.register),
    path('register/<slug:step>', views.register, name='register'),
    path('register/exhibit/<int:exhibit_id>', views.register, {'step': 'exhibit'}, name='edit_exhibit'),
    path('remove/exhibit/<int:exhibit_id>', views.remove_exhibit, name='remove_exhibit'),
    path('print', views.print, name='print'),
    path('logout/', views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
