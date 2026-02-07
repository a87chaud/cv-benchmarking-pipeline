from flask import Blueprint, request, jsonify

from app.dto.inference_dto import InferenceRequest
from app.services.services_singleton import benchmarking_service

inference_bp = Blueprint("inference", __name__, url_prefix="/inference")


# deprc i think
@inference_bp.route('/pre-process', methods=["POST"])
def pre_process():
    if "file" not in request.files:
        return jsonify({'error': 'no file'}), 400
    return {}

@inference_bp.route('/benchmarking', methods=["POST"])
def run_inference():
    '''
    Get the fields from the FE and queue a job in redis
    '''
    inference_payload = request.get_json()
    file_s3_key = inference_payload.get('file_s3_kley')
    annotation_s3_key = inference_payload.get('annotation_s3_key')
    target_latency = inference_payload.get("target_latency")
    target_accuracy = inference_payload.get("target_accuracy")
    target_hardware = inference_payload.get("target_hardware")
    inference_req = InferenceRequest(file_s3_url=file_s3_key, annotation_s3_url=annotation_s3_key, target_latency=target_latency, target_accuracy=target_accuracy, target_hardware=target_hardware)
    return jsonify(benchmarking_service.process_inference_request(inference_req))