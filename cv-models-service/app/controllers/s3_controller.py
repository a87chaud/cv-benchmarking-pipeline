from flask import Blueprint, request, jsonify
from app.services.s3_service import S3Service

s3_bp = Blueprint("s3", __name__, url_prefix="/s3")
s3_service = S3Service()
upload_id = ""
key = ""

@s3_bp.route("/get-multipart-uid", methods=["POST"])
def get_presigned_urls():
    # key = request.form['s3UploadKey']
    data = request.get_json()
    upload_id = s3_service.create_multipart_upload(data.get("s3UploadKey"))
    return {
        "uploadId": upload_id,
    }

@s3_bp.route("/generate-part-url", methods=["POST"])
def generate_part_urls():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400

    key = data.get('s3UploadKey')
    upload_id = data.get('uploadId')
    part_number = data.get('partNumber')
    if not all([key, upload_id, part_number]):
        return jsonify({"error": "Missing required fields"}), 400
    
    return s3_service.generate_part_url(key, upload_id, part_number)

@s3_bp.route('/complete-upload', methods=["POST"])
def complete_upload():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400

    key = data.get('s3UploadKey')
    upload_id = data.get('uploadId')
    parts = data.get('parts')

    if not all([key, upload_id, parts]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        result = s3_service.complete_multipart_upload(key, upload_id, parts)
        return jsonify({"message": "Upload complete", "location": result.get('Location')}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@s3_bp.route('/generate-part-url', methods=["POST"])
def generate_part_url():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400

    key = data.get('s3UploadKey')
    upload_id = data.get('uploadId')
    part_number = data.get('partNumber')
    return s3_service.generate_part_url(key, upload_id, part_number)