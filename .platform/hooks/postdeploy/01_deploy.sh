#!/bin/bash

source /var/app/venv/*/bin/activate && {

# collecting static files
python manage.py collectstatic --noinput;
# migrate
python manage.py migrate --noinput;
# another command to create a superuser (write your own)
python manage.py refresh_partners;
}
