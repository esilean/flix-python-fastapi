import logging

from decouple import config


class Config:
    version = '0.0.1'
    title = 'bevflix'

    app_settings = {
        'mongo': {
            'db_name': config('MONGO_BEVFLIX'),
            'connection_string': config('MONGO_CONNSTRING')
        },
        'credentials': {
            'secret_key': config('TOKEN_SECRET_KEY'),
            'expires_at_in_minutes': config('TOKEN_EXPIRES_AT_IN_MINUTES', default=10, cast=int)
        }
    }

    @classmethod
    def validate_app_settings(cls):
        for k, v in cls.app_settings.items():
            if v in None:
                logging.error(f'config var error. {k} cannot be None')
                raise
