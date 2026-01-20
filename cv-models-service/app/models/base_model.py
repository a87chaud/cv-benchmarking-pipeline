from abc import ABC, abstractmethod

import numpy as np

from app.utils.lookup_table import ModelInfo

class BaseModel(ABC):
    '''
    Parent class for all the models
    '''
    def __init__(self, model_info: ModelInfo):
        self.model_info = model_info
    
    @abstractmethod
    def load_model(self):
        ...
    
    @abstractmethod
    def infer(self, jpeg_bytes):
        ...
