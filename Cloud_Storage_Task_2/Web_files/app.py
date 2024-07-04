from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import boto3
import os
from werkzeug.utils import secure_filename
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Configure your AWS S3 credentials
S3_BUCKET = 'Bucket-Name'
S3_KEY = 'Public_Access_key'
S3_SECRET = 'Secret_Access_Key'
S3_REGION = 'Region-Name-of-Bucket'

s3_client = boto3.client(
    's3',
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET,
    region_name=S3_REGION
)

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    filename = secure_filename(file.filename)
    s3_client.upload_fileobj(file, S3_BUCKET, filename)
    return 'File uploaded', 200

@app.route('/download_file')
def download_file():
    filename = request.args.get('filename')
    if not filename:
        return 'Filename is required', 400
    file_obj = s3_client.get_object(Bucket=S3_BUCKET, Key=filename)
    return send_file(
        BytesIO(file_obj['Body'].read()),
        download_name=filename,
        as_attachment=True
    )

@app.route('/delete_file', methods=['DELETE'])
def delete_file():
    filename = request.args.get('filename')
    if not filename:
        return 'Filename is required', 400
    s3_client.delete_object(Bucket=S3_BUCKET, Key=filename)
    return 'File deleted', 200

@app.route('/list_files')
def list_files():
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
    files = [{'name': item['Key']} for item in response.get('Contents', [])]
    print('Files:', files)  # Debugging log
    return jsonify(files)

if __name__ == '__main__':
    app.run(debug=True)