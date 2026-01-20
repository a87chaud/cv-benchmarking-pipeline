from flask import Flask
from flask_cors import CORS 
from app.controllers.inference_controller import inference_bp
from app.controllers.s3_controller import s3_bp
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
app.register_blueprint(inference_bp)
app.register_blueprint(s3_bp)
if __name__ == '__main__':
    app.run(debug=True)
