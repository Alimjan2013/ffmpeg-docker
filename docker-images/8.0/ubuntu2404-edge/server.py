import os
import requests
from flask import Flask, request, jsonify
import ffmpeg
import uuid
import boto3
import io

app = Flask(__name__)
DOWNLOAD_DIR = '/tmp/downloads'
OUTPUT_DIR = '/tmp/outputs'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)





@app.route('/convert', methods=['POST'])
def convert():
    # Get R2/S3 credentials and config from environment
    r2_account_id = os.environ.get('R2_ACCOUNT_ID')
    r2_access_key_id = os.environ.get('R2_ACCESS_KEY_ID')
    r2_access_key_secret = os.environ.get('R2_ACCESS_KEY_SECRET')
    r2_bucket = os.environ.get('R2_BUCKET')
    r2_region = os.environ.get('R2_REGION', 'auto')
    # Compose endpoint URL
    r2_endpoint = f'https://{r2_account_id}.r2.cloudflarestorage.com'

    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No url provided'}), 400
    try:
        # Download file
        filename = str(uuid.uuid4())
        input_path = os.path.join(DOWNLOAD_DIR, filename)
        try:
            with requests.get(url, stream=True, timeout=30) as r:
                r.raise_for_status()
                with open(input_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
        except Exception as e:
            return jsonify({'error': f'Failed to download file: {str(e)}'}), 400

        # Check if file was downloaded and is not empty
        if not os.path.exists(input_path) or os.path.getsize(input_path) == 0:
            return jsonify({'error': 'Downloaded file is empty or missing'}), 400

        # Convert to 480p MP4 using x264
        output_path = os.path.join(OUTPUT_DIR, filename + '.mp4')
        try:
            stream = ffmpeg.input(input_path)
            stream = ffmpeg.output(
                stream,
                output_path,
                vcodec='libx264',
                vf='scale=-2:480',
                acodec='aac',
                audio_bitrate='128k',
                format='mp4'
            )
            ffmpeg.run(stream, overwrite_output=True)
        except Exception as e:
            return jsonify({'error': f'ffmpeg conversion failed: {str(e)}'}), 500

        # Upload to R2 via S3 protocol
        try:
            s3 = boto3.client(
                service_name="s3",
                endpoint_url=r2_endpoint,
                aws_access_key_id=r2_access_key_id,
                aws_secret_access_key=r2_access_key_secret,
                region_name=r2_region,
            )
            file_key = os.path.basename(output_path)
            with open(output_path, 'rb') as f:
                s3.upload_fileobj(f, r2_bucket, file_key)
            r2_url = f"{r2_endpoint}/{r2_bucket}/{file_key}"
        except Exception as e:
            return jsonify({'error': f'Upload to R2 failed: {str(e)}'}), 500

        return jsonify({'downloaded': input_path, 'output': output_path, 'r2_url': r2_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
