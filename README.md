# NOTOS

Django application for managing registrations for the [NOTOS 2021](http://hps.gr/notos2021/) philatelic exhibition. The application presents the user with a selection of third-party authentication options (Google, Twitter, and Facebook) and then a series of forms, organized into steps.

## Running

Start from the repository directory and create the Python environment:
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
python manage.py loaddata registrations/fixtures/federations.json
python manage.py createsuperuser
python manage.py runserver
```

And you are done. For notes on deployment, check out the [INSTALL](INSTALL.md) file.

## Customizing

To use this for other exhibitions:
* Change the exhibition name in all templates.
* Update the logo in `registrations/static/registrations/notos_2021.jpg` and the respective reference in `registrations/templates/registrations/login.html`.
* Change the `LANGUAGE_CHOICES` in `registrations/models.py` to apply to your "communication language" options.
