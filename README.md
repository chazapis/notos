# NOTOS

Django application for managing registrations for the [NOTOS 2021](http://hps.gr/notos2021/) philatelic exhibition.

## Running

Prepare the environment:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy `exhibition/settings/oauth2-empty.py` to `exhibition/settings/oauth2.py` and fill in the required keys and secrets. You have to create the appropriate applications in Google, Twitter, and Facebook.

Then, if you are developing:
```
mkdir media
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

For deployment, copy `exhibition/settings/production-empty.py` to `exhibition/settings/production.py` and fill in the settings (consult the [docs](https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/)).

Then:
```
```

## Customizing

To use this for other exhibitions:
* Update the logo in `registrations/static/registrations/notos_2021.jpg` and the respective reference in `registrations/templates/registrations/login.html`.
* Change the `LANGUAGE_CHOICES` in `registrations/models.py` to apply to your "communication language" options.
* Change the text in all templates.
