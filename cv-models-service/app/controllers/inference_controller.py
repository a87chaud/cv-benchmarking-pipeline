from flask import Blueprint, request, jsonify

from app.dto.inference_dto import InferenceRequest, JobStatus
from app.services.benchmarking_service import BenchMarkingService

inference_bp = Blueprint("inference", __name__, url_prefix="/inference")

@inference_bp.route('/pre-process', methods=["POST"])
def pre_process():
    if "file" not in request.files:
        return jsonify({'error': 'no file'}), 400
    return {}
    # start_time = time.time()
    # img_file = request.files["file"]
    # model_use_case = request.form["model_use_case"]
    # # convert it to an np array
    # file_bytes = np.frombuffer(img_file.read(), np.uint8)
    # image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    # pre_process = PreProcess(use_case=model_use_case)
    # processed_image = pre_process.execute_pipeline(image)
    # cv2 image need to convert to pil image
    # Put this all in the pre_process model

    # if len(processed_image.shape) == 2:
    #     pil_image = Image.fromarray(processed_image, mode='L')
    # else:
    #     pil_image = Image.fromarray(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))
    
    # img_io = BytesIO()
    # pil_image.save(img_io, 'PNG')
    # img_io.seek(0)
    # img_base64 = base64.b64encode(img_io.read()).decode('utf-8')
    # end_time = time.time()
    # return jsonify({
    #     'processing_time': (end_time - start_time),
    #     'objects_detected': 0,
    #     'annotated_img_url': img_base64,
    #     'model_use_case': model_use_case
    # })

@inference_bp.route('/benchmarking', methods=["POST"])
def run_inference():
    inference_payload = request.get_json()
    file_s3_key = inference_payload.get('file_s3_kley')
    annotation_s3_key = inference_payload.get('annotation_s3_key')
    target_latency = inference_payload.get("target_latency")
    target_accuracy = inference_payload.get("target_accuracy")
    target_hardware = inference_payload.get("target_hardware")
    inference_req = InferenceRequest(status=JobStatus.IN_PROGRESS, file_s3_url=file_s3_key, annotation_s3_url=annotation_s3_key, target_latency=target_latency, target_accuracy=target_accuracy, target_hardware=target_hardware)
    benchmarking_service = BenchMarkingService()
    return jsonify(benchmarking_service.return_benchmarked_results(inference_req))
    # yolo = YoloV5()
    # result = yolo.run_yolo_inference(img_file)
    # return jsonify({
    #     'processing_time': result["speed"],
    #     'objects_detected': result["boxes"],
    #     'annotated_img_url': result["image"],
    #     'model_use_case': "model_use_case"
    # })