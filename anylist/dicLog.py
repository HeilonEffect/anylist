LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/ctulhu/debug.log'
        },
        'err_log': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/ctulhu/error.log'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['file', 'err_log'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}