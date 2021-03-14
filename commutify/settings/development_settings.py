SECRET_KEY = "v=fgklxg95ztx^@=$u($41buc1pemrj6=f=y)wk5e6kuszr+iv"

DEBUG = True

ALLOWED_HOSTS = ["*"]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


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