from dataclasses import dataclass
from enum import Enum
from typing import IO

from cv2 import FileStorage

class JobStatus(Enum):
    IN_PROGRESS = 'IN_PROGRESS'
    FAILED = 'FAILED'
    DONE = 'DONE'

@dataclass
class InferenceRequest:
    status: JobStatus
    file_s3_url: str
    annotation_s3_url: str
    target_latency: int
    target_accuracy: float
    target_hardware: str
