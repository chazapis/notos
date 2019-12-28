# Copyright (C) 2019 Antony Chazapis
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.register),
    path('register/<slug:step>', views.register, name='register'),
    path('register/exhibit/<int:exhibit_id>', views.register, {'step': 'exhibit'}, name='edit_exhibit'),
    path('remove/exhibit/<int:exhibit_id>', views.remove_exhibit, name='remove_exhibit'),
    path('print', views.printout, name='print'),
    path('export', views.export, name='export'),

    path('signup', views.signup, name='signup'),
    path('activate/<slug:uidb64>/<slug:token>', views.activate, name='activate'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('reset_password/<slug:uidb64>/<slug:token>', views.reset_password, name='reset_password'),
    path('login', auth_views.LoginView.as_view(template_name='registrations/login.html'), name='login'),
    path('change_password', views.change_password, name='change_password'),
    path('logout', views.logout, {'next': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
