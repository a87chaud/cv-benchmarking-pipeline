from app.models.onnx_model import OnnxModel
from app.models.tflite_model import TfLiteModel


class ModelFactory:
    _registry = {
        "tflite": TfLiteModel,
        "onnx": OnnxModel
    }

    @classmethod
    def register(cls, framework, model_cls):
        cls._registry[framework] = model_cls

    @classmethod
    def create_model(cls, model_info):
        if model_info.framework not in cls._registry:
            raise ValueError(f"No model registered for {model_info.framework}")
        return cls._registry[model_info.framework](model_info)
