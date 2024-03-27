import os

FLASK_APP_NAME = 'csv_processing'

LOGS_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/logs/'
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'

CELERY_APP_NAME = 'csv_processing'
RABBITMQ_USER = 'guest'
RABBITMQ_PASS = 'guest'
