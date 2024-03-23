import os
from google.cloud import storage
from flask import Flask, request, jsonify, Response
import requests

import http.client
import typing
import urllib.request
import vertexai
from vertexai.generative_models import GenerativeModel, Image, Part
from io import BytesIO
app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_file():
    # Ensure both image and text are present in the request
    if 'image' not in request.files or 'text' not in request.form:
        return jsonify({"error": "Missing image or text"}), 400

    image = request.files['image']
    text = request.form['text']

    # Validate the file extension
    if image.filename.split('.')[-1].lower() not in ['jpeg', 'jpg', 'png', 'heic']:
        return jsonify({"error": "Invalid image format"}), 400

    # Prepare the files and data to be forwarded
    files = {'image': (image.filename, image.read())}
    data = {'text': text}
    image_data = image.read()
    image_data = Image.from_bytes(image_data)

    # Forward the request to the second server
    try:
        response = generate_text(
            'yuc-abhinav', 'asia-southeast1', image_data, text)
        response.raise_for_status()
        # Forward the second server's response back to the initial client
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the forwarding process
        return jsonify({"error": str(e)}), 500


def generate_text(project_id: str, location: str, img, text) -> str:
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)
    # Load the model
    vision_model = GenerativeModel("gemini-1.0-pro-vision")
    # Generate text

    response = vision_model.generate_content([

        text,        img]
    )
    print(response)
    return response.text
# Load images from Cloud Storage URI


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
