'''
This is the main server file

It allows a client to connect to google's GEMINI VISION PRO and send image data and get information from said image


developed by albertjacobsz
'''
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
@cross_origin()
def upload_file():
    # Ensure both image and text are present in the request
    if 'image' not in request.files or 'text' not in request.form:
        return jsonify({"error": "Missing image or text"}), 400
    print(f"request noted: {request}")
    image = request.files['image']
    text = request.form['text']

    # Validate the file extension
    if image.filename.split('.')[-1].lower() not in ['jpeg', 'jpg', 'png', 'heic']:
        return jsonify({"error": "Invalid image format"}), 400
    # Prepare the files and data to be forwarded

    content = request.files.get('image').read()

    files = {'image': (image.filename, image.read())}
    data = {'text': text}

    url = upload_picture_to_gcs(content, image.filename)
    # Forward the request to the second server
    try:
        txt = generate_text(
            'yuc-abhinav', 'asia-southeast1', url, text)
        print(f"type: {type(response.text)}")
        print(f"got response: {response.text}")
        response = jsonify(message=txt)
        # Forward the second server's response back to the initial client
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
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

    return response


# Load images from Cloud Storage URI
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
