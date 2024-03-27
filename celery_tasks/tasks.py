from celery import Celery

from csv_processing.csv_processing import LargeCSVProcessor

app = Celery('csv_processing', broker='amqp://guest:guest@127.0.0.1:5672//',
             backend='rpc://')


@app.task(bind=True)
def process_large_csv_task(self, input_file, output_file):
    processor = LargeCSVProcessor(input_file, output_file)
    processor.process_data()
