from pathlib import Path
import accounting.apps
import cart.apps
import home.apps
import order.apps

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-(mod)=0sm*jqdxgds8pmsh)x5od9g7%#l8f_2+f^#puecr&c0e'

DEBUG = True
ALLOWED_HOSTS = []

# to see 404 Page
# DEBUG = False
# ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    # 'jazzmin',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'ckeditor',
    'ckeditor_uploader',
    'taggit',
    'sorl.thumbnail',
    'django_jalali',
    'django_filters',
    'accounting.apps.AccountingConfig',
    'home.apps.HomeConfig',
    'cart.apps.CartConfig',
    'order.apps.OrderConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_db',
        'USER': 'mohammad',
        'PASSWORD': '1234',
        'HOST': 'db',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

""" Media and Static """

STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

""" Ckeditor Configs  """
CKEDITOR_UPLOAD_PATH = 'ck/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}
""" Taggit """
TAGGIT_CASE_INSENSITIVE = True

""" Sending Email Configs """
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'amirimohammad117@gmail.com'
EMAIL_HOST_PASSWORD = 'evkqsnpwdpfjzsfy'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
