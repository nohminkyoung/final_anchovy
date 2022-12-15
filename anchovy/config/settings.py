"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import pymysql

pymysql.install_as_MySQLdb()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zc*&$wzh0#@s#(aqrczz(i%+aud4$r31=gi-^bf6*m20-8q1g*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'anchovy_common.Custom_User'
# Application definition

INSTALLED_APPS = [
    # 데이터 베이스 이용 시. 각 폴더에서 apps.py를 들어가 이름을 찾고 아래와 같이 추가를 해야 한다.
    #'training.apps.TrainingConfig', : 예시 문구
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'anchovy_common.apps.AnchovyCommonConfig',
    'anchovy_main.apps.AnchovyMainConfig',
    'anchovy_notice.apps.AnchovyNoticeConfig',
    'anchovy_settings.apps.AnchovySettingsConfig',
    'anchovy_train.apps.AnchovyTrainConfig',
    'anchovy_user.apps.AnchovyUserConfig'
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME" : "anchovy_db",
        "USER" : 'develop',
        "PASSWORD" : 'anchovy1!',
        'HOST' : 'database-dev.cclpxl5ttlgd.ap-northeast-2.rds.amazonaws.com',
        'PORT' : '3306'
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    # 공통 static
    os.path.join(BASE_DIR, 'static'),
    
    # 개별 static
    os.path.join(BASE_DIR,'anchovy_common', 'static'),
    os.path.join(BASE_DIR,'anchovy_main', 'static'),
    os.path.join(BASE_DIR,'anchovy_notice', 'static'),
    os.path.join(BASE_DIR,'anchovy_settings', 'static'),
    os.path.join(BASE_DIR,'anchovy_train', 'static'),
    os.path.join(BASE_DIR,'anchovy_user', 'static'),
    
]

