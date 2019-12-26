# INSTALL

## Development

Start from the repository directory and create the Python environment:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then:
```
mkdir media
python manage.py migrate
python manage.py loaddata registrations/fixtures/federations.json
python manage.py createsuperuser
python manage.py runserver
```

And you are done. Consult `exhibition/settings/default.py` for available configuration options.

## Production

What follows are some notes on how to deploy NOTOS for "production". They will most surely need adjustments depending on your actual environment and needs.

I assume a Debian/Ubuntu system and the code checked out in `/srv/` (edit the scripts to change).

Start from the repository directory and create the Python environment:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy `exhibition/settings/production-empty.py` to `exhibition/settings/production.py` and fill in the settings (consult the [docs](https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/)). To enable external authentication you have to create the appropriate applications in Google, Twitter, or Facebook and fill in the required keys and secrets.

Then:
```
export DJANGO_SETTINGS_MODULE=exhibition.settings.production
mkdir media
chown www-data:www-data media
mkdir static
python manage.py collectstatic
python manage.py migrate
python manage.py loaddata registrations/fixtures/federations.json
chown www-data:www-data . db.sqlite3
python manage.py createsuperuser
```

Edit `scripts/apache2/exhibition.conf` for your domain (you may also need to set a dummy `ServerName` in `/etc/apache2/sites-available/000-default.conf`).

Then:
```
apt-get install supervisor
cp scripts/supervisor/exhibition.conf /etc/supervisor/conf.d/
supervisorctl reload

apt-get install apache2
cp scripts/apache2/exhibition.conf /etc/apache2/sites-available/
a2enmod proxy_http
a2enmod headers
a2ensite exhibition
service apache2 restart
```

Make sure it works, then enable SSL:
```
apt-get install python3-certbot-apache
certbot --apache -d <your.domain>
```

`certbot` will get the certificate, update the Apache configuration to redirect all traffic to HTTPS, and even install a cron script to renew the certificate when necessary.

Done!
