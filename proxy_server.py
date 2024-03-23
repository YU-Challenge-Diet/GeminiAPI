from flask import Flask, request, jsonify, Response
import requests

import http.client
import typing
import urllib.request

from vertexai.generative_models import GenerativeModel, Image
app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_file():
    # Ensure both image and text are present in the request
    if 'image' not in request.files or 'text' not in request.form:
        return jsonify({"error": "Missing image or text"}), 400

    image = request.files['image']
    text = request.form['text']

    # Validate the file extension
    if image.filename.split('.')[-1].lower() not in ['jpg', 'png', 'heic']:
        return jsonify({"error": "Invalid image format"}), 400

    # Prepare the files and data to be forwarded
    files = {'image': (image.filename, image.read())}
    data = {'text': text}

    # Forward the request to the second server
    try:
        # Assuming the second server is expecting the image as a multipart/form-data
        # and the text as form data
        # Pass multimodal prompt
        model = GenerativeModel("gemini-1.0-pro-vision")
        response = model.generate_content(
            [
                image.read(),
                text

            ]
        )
        print(response)
        response.raise_for_status()
        # Forward the second server's response back to the initial client
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the forwarding process
        return jsonify({"error": str(e)}), 500


# Load images from Cloud Storage URI


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
