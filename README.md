# Exhibition

Django application for managing registrations for the [NOTOS 2021](http://hps.gr/notos2021/) philatelic exhibition.

## Running

Prepare the environment:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy `exhibition/oauth2-empty.py` to `exhibition/oauth2.py` and fill in the required keys and secrets. You have to create the appropriate applications in Google and Twitter.

Then:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Customizing

To use this for other exhibitions:
* Update the logo in `registrations/static/registrations/notos_2021.jpg` and the respective reference in `registrations/templates/registrations/login.html`.
* Change the `LANGUAGE_CHOICES` in `registrations/models.py` to apply to your "communication language" options.
* Change the text in all templates.
