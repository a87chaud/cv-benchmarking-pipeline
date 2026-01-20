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
    file: bytes
    target_latency: int
    target_accuracy: float
    target_hardware: str
