from celery import Celery

from config import CELERY_APP_NAME, RABBITMQ_USER, RABBITMQ_PASS
from csv_processing.csv_processing import LargeCSVProcessor

app = Celery(CELERY_APP_NAME,
             broker=f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@127.0.0.1:5672/',
             backend='rpc://')


@app.task(bind=True)
def process_large_csv_task(self, input_file, output_file):
    processor = LargeCSVProcessor(input_file, output_file)
    processor.process_data()
