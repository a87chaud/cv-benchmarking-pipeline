from dataclasses import dataclass
from enum import Enum
from typing import Optional
from app.utils.lookup_table import ModelInfo

class JobStatus(Enum):
    QUEUED = 'QUEUED'
    PROCESSING = 'PROCESSING'
    FAILED = 'FAILED'
    DONE = 'DONE'

@dataclass
class InferenceRequest:
    file_s3_url: str
    annotation_s3_url: str
    target_latency: int
    target_accuracy: float
    target_hardware: str

@dataclass 
class RedisJob:
    status: JobStatus
    file_s3_url: str
    annotation_s3_url: str
    target_latency: int
    target_accuracy: float
    target_hardware: str
    model_zoo: list[ModelInfo]
    job_id: str
