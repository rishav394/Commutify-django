# Commutify-django

REST server for [Commutify](https://github.com/rishav394/Commutify) app

## How to run locally

### Prerequisite
1. Python >3.6
2. MySQL >5.7
3. `mysql -> CREATE DATABASE commutify_db;`

### Setup and Run
```bash
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
cp commutify/settings/development_settings.py commutify/settings/production_settings.py
cp commutify/settings/settings.py.bak commutify/settings/settings.py
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Running on production
Same setup as local but make sure to make changes to `production_settings.py`
