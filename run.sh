python3 -m venv virtualenv
cd devpro

source ../virtualenv/bin/activate
pip install -r requirements.txt


mkdir /srv/projects/devpro/backend/media
chown -R www-data:www-data /srv/projects/devpro/backend/media

cd /srv/projects/devpro/backend
source /srv/projects/devpro/virtualenv/bin/activate
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py sync_translation_fields --noinput
python manage.py update_translation_fields
python manage.py createsuperuser --username testuser --email root@local.host
deactivate

service nginx restart &
service uwsgi restart &
service supervisor restart


server {
    server_name test.uz ;

    listen 46.36.217.216:80;

    charset utf-8;
    gzip on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private auth;
    gzip_types text/css image/x-ico application/pdf image/jpeg image/png image/gif application/javascript application/x-javascript application/x-pointplus;
    gzip_comp_level 1;

    set $root_path /srv/projects/devpro;

    root $root_path;
    disable_symlinks if_not_owner from=$root_path;

    location / {
	    proxy_bind 127.0.0.1;
        proxy_set_header   Host $host;
        proxy_pass         http://127.0.0.1:8000;
        index index.html;
    }
