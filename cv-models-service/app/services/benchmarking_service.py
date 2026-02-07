from typing import List
from app.dto.inference_dto import InferenceRequest
from app.utils.model_factory import ModelFactory
from app.services.s3_service import S3Service
from app.services.redis_service import RedisService
from app.services.services_singleton import redis_service

class BenchMarkingService:
    '''
    Service to handle 
    1. Orchestration to redis queue
    2. Processing of results 
    and more stuff probably
    '''
    def process_inference_request(self, inference_req: InferenceRequest) -> str: 
        return redis_service.enqueue_inference_req(inference_req)


    
    # def return_benchmarked_results(self, inference_req: InferenceRequest):
    #     target_hardware: Hardware = Hardware[inference_req.target_hardware]
    #     models_to_run: List[ModelInfo] = HardwareLookUp.get_candidate_models(target_hardware)
    #     responses = []
    #     for model_info in models_to_run:
    #         curr_runner = ModelFactory.create_model(model_info=model_info)
    #         detections_raw = curr_runner.infer(inference_req.file)
    #         labels = ['Dog']
    #         det_final = curr_runner.post_process(detections_raw, labels)
    #         annotated_img_b64 = curr_runner.get_annotated_image(det_final)
    #         responses.append({
    #                 "processing_time_ms" : 0,
    #                 "objects_detected": 69,
    #                 "annotated_img_url": annotated_img_b64,
    #             })
        
    #     return responses[0]