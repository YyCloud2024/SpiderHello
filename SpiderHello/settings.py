import os
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c9@8e5j4$eadq-iw-s-(x#)$bia^g2(@p(%y)#1vjwek4qwa^y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

# 跨域设置
SECURE_CROSS_ORIGIN_OPENER_POLICY = "None"
# 跨域请求配置，允许所有源的跨域请求
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True




# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'BloodSpiderAPI.apps.BloodSpiderAPIConfig',
    'BloodSpiderWeb.apps.BloodspiderwebConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'BloodSpiderAPI.middlewares.PathManage.PathManage',
]

ROOT_URLCONF = 'SpiderHello.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': []
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SpiderHello.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'SpiderHello',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = False

# 静态文件配置
"""
如果是在本地开发,推荐 STATIC_ROOT = os.path.join(BASE_DIR, 'BloodSpiderWeb/static')
如果是部署到服务器, 推荐 STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
    部署前运行python manage.py collectstatic命令
"""
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'BloodSpiderWeb/static')
# STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "BlackWidow",'static'),
# ]


# 主键字段类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 媒体文件配置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# 当前版本
SPIDERHELLO_VERSION = '1.0.0'

# 管理员微信
ADMIN_WECHAT = 'duyanbz'