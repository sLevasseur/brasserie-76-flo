#!/bin/sh
# shellcheck disable=SC2039
set -eu pipefail
python3 manage.py collectstatic --noinput

#echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('adm_simon', 'simonphilippe.levasseur@gmail.com', 'ersoulerin')" | python manage.py shell || None

python3 manage.py makemigrations

python3 manage.py migrate

#sudo service postgresql restart

exec python3 manage.py runserver 0:8000
