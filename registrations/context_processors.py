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

from django.conf import settings


def exhibition(request):
    return {'exhibition_name': settings.EXHIBITION_NAME,
            'exhibition_url': settings.EXHIBITION_URL,
            'exhibition_email': settings.EXHIBITION_EMAIL,
            'exhibition_logo': settings.EXHIBITION_LOGO}

def oauth(request):
    auth_google = (settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY and settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET)
    auth_twitter = (settings.SOCIAL_AUTH_TWITTER_KEY and settings.SOCIAL_AUTH_TWITTER_SECRET)
    auth_facebook = (settings.SOCIAL_AUTH_FACEBOOK_KEY and settings.SOCIAL_AUTH_FACEBOOK_SECRET)
    auth_social = (auth_google or auth_twitter or auth_facebook)
    return {'auth_google': auth_google,
            'auth_twitter': auth_twitter,
            'auth_facebook': auth_facebook,
            'auth_social': auth_social}
