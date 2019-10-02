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

And you are done.

For deployment, assuming a Debian/Ubuntu system and the code checked out in `/srv/` (edit the scripts to change), instead of the above do:

```
export DJANGO_SETTINGS_MODULE=exhibition.settings.production
mkdir media
chown www-data:www-data media
mkdir static
python manage.py collectstatic
python manage.py migrate
chown www-data:www-data db.sqlite3
python manage.py createsuperuser
```

Copy `exhibition/settings/production-empty.py` to `exhibition/settings/production.py` and fill in the settings (consult the [docs](https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/)).

Edit `scripts/apache2/exhibition.conf` for your domain (you may also need to set a dummy `ServerName` in `/etc/apache2/sites-available/000-default.conf`).

Then:
```
apt-get install supervisor
cp scripts/supervisor/* /etc/supervisor/conf.d/
supervisorctl reload

apt-get install apache2
cp scripts/apache2/* /etc/apache2/sites-available/
a2enmod proxy_http
a2ensite exhibition
service apache2 reload
```

## Customizing

To use this for other exhibitions:
* Update the logo in `registrations/static/registrations/notos_2021.jpg` and the respective reference in `registrations/templates/registrations/login.html`.
* Change the `LANGUAGE_CHOICES` in `registrations/models.py` to apply to your "communication language" options.
* Change the text in all templates.
