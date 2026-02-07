import redis
import json
import uuid
from datetime import datetime
from app.dto.inference_dto import InferenceRequest, RedisJob, JobStatus
from app.utils.lookup_table import HardwareLookUp, Hardware
from dataclasses import asdict

class RedisService:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
    
    def enqueue_inference_req(self, inference_req: InferenceRequest) -> str:
        job_id = str(uuid.uuid4())
        target_hardware = Hardware[inference_req.target_hardware]
        model_zoo = HardwareLookUp.get_candidate_models(target_hardware)
        new_job = RedisJob(
            status=JobStatus.QUEUED,
            file_s3_url=inference_req.file_s3_url,
            annotation_s3_url=inference_req.annotation_s3_url,
            target_latency=inference_req.target_latency,
            target_accuracy=inference_req.target_accuracy,
            target_hardware=inference_req.target_hardware,
            model_zoo=model_zoo,
            job_id=job_id
        )

        self.client.hset(f"job:{job_id}", mapping=asdict(new_job))

        # 3. Push only the job_id to the hardware-specific List (The "Notification")
        queue_name = f"queue:{inference_req.target_hardware}"
        self.client.lpush(queue_name, job_id)

        return job_id
    
    def get_job_status(self, job_id: str) -> dict:
        return self.client.hgetall(f"job:{job_id}") # type: ignore