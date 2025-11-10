from flask import Flask, request, jsonify
from flask_cors import CORS 
import cv2
import numpy as np
from PIL import Image
from models.pre_process import PreProcess
import base64
from io import BytesIO
import time

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:4200",
            "http://127.0.0.1:4200"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
@app.route('/', methods=["GET"])
def main():
    return jsonify({"home"}), 200
'''
1. Need to make a new class for the request this is terrible but okay for now
'''
@app.route('/pre-process', methods=["POST"])
def pre_process():
    if "file" not in request.files:
        return jsonify({'error': 'no file'}), 400
    start_time = time.time()
    img_file = request.files["file"]
    model_use_case = request.form["model_use_case"]
    # convert it to an np array
    file_bytes = np.frombuffer(img_file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    pre_process = PreProcess(use_case=model_use_case)
    processed_image = pre_process.execute_pipeline(image)

    # cv2 image need to convert to pil image
    # Put this all in the pre_process model
    if len(processed_image.shape) == 2:
        pil_image = Image.fromarray(processed_image, mode='L')
    else:
        pil_image = Image.fromarray(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))
    
    img_io = BytesIO()
    pil_image.save(img_io, 'PNG')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.read()).decode('utf-8')
    end_time = time.time()
    return jsonify({
        'processing_time': (end_time - start_time),
        'objects_detected': 0,
        'annotated_img_url': img_base64,
        'model_use_case': model_use_case
    })
if __name__ == '__main__':
    app.run(debug=True)
