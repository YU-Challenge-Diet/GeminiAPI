import os
from google.cloud import storage
from flask import Flask, request, jsonify, Response
import requests
import http.client
import typing
import urllib.request
import vertexai
from io import BufferedReader
from vertexai.generative_models import GenerativeModel, Image, Part
from io import BytesIO
app = Flask(__name__)


def upload_picture_to_gcs(picture_data, filename):
    # Set up the Google Cloud Storage client
    client = storage.Client()

    # Specify the bucket name and file name
    bucket_name = "gemini_bucket_1"
    file_name = filename  # Specify the desired file name

    # Get the bucket and create a new blob
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Upload the picture data to Google Cloud Storage
    blob.upload_from_string(picture_data, content_type='image/png')

    # Get the public URL of the uploaded file
    url = 'gs://gemini_bucket_1/'+file_name

    return url


@app.route('/upload', methods=['POST'])
def upload_file():
    # Ensure both image and text are present in the request
    if 'image' not in request.files or 'text' not in request.form:
        return jsonify({"error": "Missing image or text"}), 400
    print(f"New request {request}")
    image = request.files['image']
    text = request.form['text']
    print(f"image: {image}")
    # Validate the file extension
    if image.filename.split('.')[-1].lower() not in ['jpeg', 'jpg', 'png', 'heic']:
        return jsonify({"error": "Invalid image format"}), 400
    # Prepare the files and data to be forwarded
    files = {'image': (image.filename, image.read())}
    data = {'text': text}
    image = request.files.get('image')
    image.name = image.filename
    image = BufferedReader(image)

    print(f"image: {image}")
    url = upload_picture_to_gcs(image, image.name)
    print(f"The url is {url}")

    # Forward the request to the second server
    try:
        response = generate_text(
            'yuc-abhinav', 'asia-southeast1', url, text)
        response.raise_for_status()
        # Forward the second server's response back to the initial client
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the forwarding process
        return jsonify({"error": str(e)}), 500


def generate_text(project_id: str, location: str, url, text) -> str:

    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)
    # Load the model
    vision_model = GenerativeModel("gemini-1.0-pro-vision")
    # Generate text
    response = vision_model.generate_content(
        [
            Part.from_uri(
                url, mime_type="image/png"
            ),
            text,
        ]
    )
    print(response)
    return response.text


# Load images from Cloud Storage URI
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
