import os
from uuid import uuid4

from flask import Flask, request, jsonify, send_file
from config import FLASK_APP_NAME, UPLOAD_FOLDER, DOWNLOAD_FOLDER
from celery_tasks.tasks import process_large_csv_task

app = Flask(FLASK_APP_NAME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def schedule_processing():
    # Check if file is present in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    # generate task id in advance to create associated input/output files
    task_id = str(uuid4())

    # Save the uploaded file in common location
    input_file = f'{app.config["UPLOAD_FOLDER"]}{task_id}_input.csv'
    file.save(input_file)

    output_file = f'{app.config["DOWNLOAD_FOLDER"]}{task_id}_output.csv'

    # Start Celery task to handle file processing asynchronously
    task = process_large_csv_task.apply_async((input_file, output_file),
                                              task_id=task_id)

    return jsonify({'task_id': task.id}), 200


@app.route('/download/<task_id>', methods=['GET'])
def download_result(task_id):
    # Check if Celery task with task_id exists
    task = process_large_csv_task.AsyncResult(task_id)

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
