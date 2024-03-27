import os
from pathlib import Path

from uuid import uuid4

from flask import Flask, request, jsonify, send_file
from celery_tasks.tasks import process_large_csv_task

app = Flask('csv_processing')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
app.config['UPLOAD_FOLDER'] = f'{BASE_DIR}/uploads'
app.config['DOWNLOAD_FOLDER'] = f'{BASE_DIR}/downloads'


@app.route('/upload', methods=['POST'])
def schedule_processing():
    # Check if file is present in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    # Save the uploaded file in common location
    input_file_path = f'uploads/{file.filename}'
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    task_id = str(uuid4())
    output_file_path = f'downloads/{task_id}_output.csv'
    print(task_id)
    # Start Celery task to handle file processing asynchronously
    task = process_large_csv_task.apply_async((input_file_path, output_file_path), task_id=task_id)

    return jsonify({'task_id': task.id}), 200


@app.route('/download/<task_id>', methods=['GET'])
def download_result(task_id):
    # Check if Celery task with task_id exists
    task = process_large_csv_task.AsyncResult(task_id)
    print(task)
    if task.state == 'processing':
        return jsonify({'status': 'Processing', 'message': 'Task is still in progress'}), 202
    elif task.state == 'FAILURE':
        return jsonify({'status': 'Failed', 'message': 'Task failed to complete'}), 500

    # Check if processing is complete (output file exists)
    output_file = os.path.join(app.config['DOWNLOAD_FOLDER'], f'{task_id}_output.csv')
    if not os.path.exists(output_file):
        return jsonify({'status': 'Processing', 'message': 'Output file not available yet'}), 202

    # Download the resulting CSV file
    return send_file(output_file, as_attachment=True, download_name='output.csv')
