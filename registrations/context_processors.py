from django.conf import settings

def oauth(request):
    auth_google = (settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY and settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET)
    auth_twitter = (settings.SOCIAL_AUTH_TWITTER_KEY and settings.SOCIAL_AUTH_TWITTER_SECRET)
    auth_facebook = (settings.SOCIAL_AUTH_FACEBOOK_KEY and settings.SOCIAL_AUTH_FACEBOOK_SECRET)
    auth_social = (auth_google or auth_twitter or auth_facebook)
    return {'auth_google': auth_google,
            'auth_twitter': auth_twitter,
            'auth_facebook': auth_facebook,
            'auth_social': auth_social}
