from pathlib import Path
import os
BASE_DIR=Path(__file__).resolve().parent.parent
SECRET_KEY=os.environ.get("DJANGO_SECRET_KEY","dev-only-change-me")
DEBUG=os.environ.get("DJANGO_DEBUG","0")=="1"
ALLOWED_HOSTS=[h.strip() for h in os.environ.get("DJANGO_ALLOWED_HOSTS","perfectsolution.smarbiz.sbs,localhost,127.0.0.1").split(",") if h.strip()]
CSRF_TRUSTED_ORIGINS=["https://perfectsolution.smarbiz.sbs","http://perfectsolution.smarbiz.sbs"]
INSTALLED_APPS=["django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles","shop"]
MIDDLEWARE=["django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware","django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF="perfectsolution.urls"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[BASE_DIR/"templates"],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION="perfectsolution.wsgi.application"
DATABASES={"default":{"ENGINE":"django.db.backends.sqlite3","NAME":os.environ.get("SQLITE_PATH",BASE_DIR/"db.sqlite3")}}
AUTH_PASSWORD_VALIDATORS=[]
LANGUAGE_CODE="de-de"
TIME_ZONE="Europe/Berlin"
USE_I18N=True
USE_TZ=True
STATIC_URL="/static/"
STATIC_ROOT=BASE_DIR/"staticfiles"
STATICFILES_DIRS=[BASE_DIR/"static"]
MEDIA_URL="/media/"
MEDIA_ROOT=Path(os.environ.get("MEDIA_ROOT",BASE_DIR/"media"))
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
SESSION_COOKIE_SECURE=os.environ.get("DJANGO_SECURE","1")=="1"
CSRF_COOKIE_SECURE=SESSION_COOKIE_SECURE
SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO","https")
