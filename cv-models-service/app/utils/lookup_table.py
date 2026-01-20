from enum import Enum
from dataclasses import dataclass

class Hardware(str, Enum):
    RPI = "rpi"
    JETSON_NANO = "jetson_nano"
    JETSON_XAVIER = "jetson_xavier"
    CPU = "cpu"
    EDGE_TPU = "edge_tpu"

class Framework(str, Enum):
    TFLite = "tflite"
    Onnx = "Onnx"

@dataclass
class ModelInfo:
    name: str
    framework: str
    task: str
    quantized: bool
    artifact: str
    input_shape: tuple

class HardwareLookUp:

    LOOKUP_TABLE = {
        Hardware.RPI: [
            # ModelInfo(
            #     name="mobilenet_v2",
            #     framework="tflite",
            #     task="classification",
            #     quantized=True,
            #     artifact="mobilenet_v1_1.0_224_quant.tflite",
            #     input_shape=(224, 224, 3)
            # ),
            # ModelInfo(
            #     name="mobilenet_v3_small",
            #     framework="tflite",
            #     task="classification",
            #     quantized=True,
            #     artifact="mobilenet_v3_small.tflite",
            #     input_shape=(224, 224, 3)
            # ),
            # ModelInfo(
            #     name="efficientnet_lite0",
            #     framework="tflite",
            #     task="classification",
            #     quantized=True,
            #     artifact="efficientnet_lite0.tflite",
            #     input_shape=(224, 224, 3)
            # ),
            ModelInfo(
                name="yolov5",
                framework="onnx",
                task="detection",
                quantized=False,
                artifact="yolov5m.onnx",
                input_shape=(640, 640, 3)
            ),
            # ModelInfo(
            #     name="yolov8n",
            #     framework="onnx",
            #     task="detection",
            #     quantized=False,
            #     artifact="yolov8n.onnx",
            #     input_shape=(640, 640, 3)
            # ),
        ],

        Hardware.JETSON_NANO: [
            ModelInfo(
                name="yolov5n",
                framework="tensorrt",
                task="detection",
                quantized=False,
                artifact="yolov5n.engine",
                input_shape=(640, 640, 3)
            ),
            ModelInfo(
                name="yolov8n",
                framework="tensorrt",
                task="detection",
                quantized=False,
                artifact="yolov8n.engine",
                input_shape=(640, 640, 3)
            ),
            ModelInfo(
                name="ssd_mobilenet",
                framework="tensorrt",
                task="detection",
                quantized=True,
                artifact="ssd_mobilenet.engine",
                input_shape=(300, 300, 3)
            ),
            ModelInfo(
                name="efficientdet_d0",
                framework="tensorrt",
                task="detection",
                quantized=False,
                artifact="efficientdet_d0.engine",
                input_shape=(512, 512, 3)
            ),
        ],

        Hardware.JETSON_XAVIER: [
            ModelInfo(
                name="yolov5s",
                framework="tensorrt",
                task="detection",
                quantized=False,
                artifact="yolov5s.engine",
                input_shape=(640, 640, 3)
            ),
            ModelInfo(
                name="yolov8s",
                framework="tensorrt",
                task="detection",
                quantized=False,
                artifact="yolov8s.engine",
                input_shape=(640, 640, 3)
            ),
            ModelInfo(
                name="yolov7_tiny",
                framework="tensorrt",
                task="detection",
                quantized=False,
                artifact="yolov7_tiny.engine",
                input_shape=(640, 640, 3)
            ),
            ModelInfo(
                name="efficientdet_d1",
                framework="tensorrt",
                task="detection",
                quantized=False,
                artifact="efficientdet_d1.engine",
                input_shape=(640, 640, 3)
            ),
            ModelInfo(
                name="resnet18",
                framework="onnx",
                task="classification",
                quantized=False,
                artifact="resnet18.onnx",
                input_shape=(224, 224, 3)
            ),
        ],

        Hardware.CPU: [
            ModelInfo(
                name="resnet18",
                framework="onnx",
                task="classification",
                quantized=False,
                artifact="resnet18.onnx",
                input_shape=(224, 224, 3)
            ),
            ModelInfo(
                name="efficientnet_b0",
                framework="onnx",
                task="classification",
                quantized=False,
                artifact="efficientnet_b0.onnx",
                input_shape=(224, 224, 3)
            ),
            ModelInfo(
                name="yolov5s",
                framework="onnx",
                task="detection",
                quantized=False,
                artifact="yolov5s.onnx",
                input_shape=(640, 640, 3)
            ),
            ModelInfo(
                name="yolov8s",
                framework="onnx",
                task="detection",
                quantized=False,
                artifact="yolov8s.onnx",
                input_shape=(640, 640, 3)
            ),
        ],

        Hardware.EDGE_TPU: [
            ModelInfo(
                name="mobilenet_v2_edgetpu",
                framework="tflite",
                task="classification",
                quantized=True,
                artifact="mobilenet_v2_edgetpu.tflite",
                input_shape=(224, 224, 3)
            ),
            ModelInfo(
                name="mobilenet_v3_small_edgetpu",
                framework="tflite",
                task="classification",
                quantized=True,
                artifact="mobilenet_v3_small_edgetpu.tflite",
                input_shape=(224, 224, 3)
            ),
            ModelInfo(
                name="efficientdet_lite0_edgetpu",
                framework="tflite",
                task="detection",
                quantized=True,
                artifact="efficientdet_lite0_edgetpu.tflite",
                input_shape=(512, 512, 3)
            ),
        ],
    }


    @classmethod
    def get_candidate_models(cls, hardware: Hardware):
        return cls.LOOKUP_TABLE.get(hardware, [])
