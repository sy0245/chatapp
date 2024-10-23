from .settings_common import *
import os
# SECRET_KEY = 'django-insecure-ozyl(r!*=wht$a7^pp+wp=zg5g96yg5wz!7fwe$gq63874z9##'
# DEBUG = True
# ALLOWED_HOSTS = []

DEBAG=os.getenv("DEBUG","y")
CROS_ALLOW_ALL_ORIGINS=DEBUG

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'chatapp_db',
        'USER': 'sy0245',
        'PASSWORD': '0245',
        'HOST': 'localhost',
        'PORT': '5432',
    }
    
    
}



# LOGGING={
#     "version":1,
#     "disable_exisiting_loggers":False,
#     "loggers":{
#         "django":{
#             "handlers":["console"],
#             "level":"INFO",
#         },
#         "myapp":{
#             "handlers":["console"],
#             "level":"DEBUG",
#         },
#     },

#     "handlers":{
#             "console":{
#             "lebel":"DEBUG",
#             "class":"logging.StreamHandler",
#             "formatter":"dev"
#         },
#     },
#     "formatters":{
#         "dev":{
#             "format":"\t".join(["%'asctime)s","[%(levelname)s]","%(pathname)s(Line:%(lineno)d)","%(message)s"])
#         },
#     }
# }
# EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend"