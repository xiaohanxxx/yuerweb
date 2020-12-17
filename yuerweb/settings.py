"""
Django settings for yuerweb project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b#b^v39c)n1)6jg52gq@%m1q(paqhd5mrv5(y6!9*1yo!g+=4+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'simpleui',  # 后台模板
    'notifications', # 通知功能
    'users', # 用户app
    'luntan',
    'hospital',
    'shiguanbaby',
    'taolun',
    'baike', # 百科app
    'webmanage', # 网站管理 app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',  # 后台富文本编辑器
    'ckeditor_uploader',  # 后台富文本编辑器上传图片模块
    'haystack'
]

# 富文本编辑器配置
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 400,
        'width': 1000,
    },
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'yuerweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'template')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'yuerweb.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'yuer_data',
#         'HOST': '139.155.251.141',
#         'PORT': '3306',
#         'USER': 'root',
#         'PASSWORD': 'tbr@123456..',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yuer_data',
        'HOST': '139.155.251.141',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'tbr@123456..',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'yuer_data',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#         'USER': 'root',
#         'PASSWORD': '123456',
#     }
# }


HAYSTACK_CONNECTIONS = {
    'default': {
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'ENGINE': 'haystack.backends.whoosh_ch_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
#         'URL': 'http://127.0.0.1:9200/',
#         'INDEX_NAME': 'haystack',
#     },
# }


HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10

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
# # https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
CKEDITOR_UPLOAD_PATH = "images"  # 上传图片保存路径

LOGIN_URL = '/login'

# 帖子分页
PAGE_NUM = 10


# 短信验证
#SMS_SECRET_ID = "AKID2rPgnI0VChz0lVAIQIMCoFTSBdonM96t"  # API秘钥管理SecretId
#SMS_SECRET_KEY = "lKsAGxQdeOuCF9nBQVMAi2RaVBiyHK7q"  # API秘钥管理SecretKey
#SMS_APPID = '1400447111'  # 应用列表SDK AppID
#SMS_SIGN = '智媒AI批量写作助手'  # 签名管理的内容

# 正文模板管理ID
#SMS_TEMPLATE_ID = {
#    'test1': '770865',  # 注册模板ID
#    'register': '770682',  # 注册模板ID
#    # 'register': '123456',  # 注册模板ID
#    # 're_password': '123456',  # 改密模板ID
#}

# 短信验证
SMS_SECRET_ID = "AKIDh8IC2zP4CblcChp3pKcxB9ukLehXLRUT"  # API秘钥管理SecretId
SMS_SECRET_KEY = "FKJw461qW3ZcqOp9gGxY0Ys6EOOPOr4h"  # API秘钥管理SecretKey
SMS_APPID = '1400460735'  # 应用列表SDK AppID
SMS_SIGN = '孕儿网'  # 签名管理的内容

# 正文模板管理ID
SMS_TEMPLATE_ID = {
    'test1': '804921',  # 修改密码模板id
    'register': '804915',  # 注册模板ID
    # 'register': '123456',  # 注册模板ID
    # 're_password': '123456',  # 改密模板ID
}

AUTH_PROFILE_MODULE = 'djangoadmin.users.Userinfo' # User扩展表userinfo

