### Setup Steps
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

## Run server
source env/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver