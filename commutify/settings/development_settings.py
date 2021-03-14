# Use this in development
# Rename it to production_settings.py and set DEBUG to false to use in Production

SECRET_KEY = "v=fgklxg95ztx^@=$u($41buc1pemrj6=f=y)wk5e6kuszr+iv"

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "commutify_db",
        "USER": "root",
        "PASSWORD": "root",
        "HOST": "",
        "PORT": "",
        "CONN_MAX_AGE": 60,
    },
}