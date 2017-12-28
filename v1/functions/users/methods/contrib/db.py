import os
from orator import DatabaseManager

db = DatabaseManager({
    'default': 'mysql',
    'mysql': {
        'driver': 'mysql',
        'host': os.environ.get('MySQL_HOST') or 'localhost',
        'database': os.environ.get('MySQL_DATABASE') or 'zeitstories',
        'user': os.environ.get('MySQL_USER') or 'root',
        'password': os.environ.get('MySQL_PASSWORD') or 'mysql',
        'use_qmark': True,
    }
})
