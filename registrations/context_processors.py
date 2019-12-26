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
