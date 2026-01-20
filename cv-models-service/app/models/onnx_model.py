import cv2
import numpy as np
import onnxruntime as ort
import base64
from pathlib import Path
from app.models.base_model import BaseModel

class OnnxModel(BaseModel):
    def __init__(self, model_info):
        super().__init__(model_info=model_info)
        self.load_model()
        self.orig_img = None 

    def load_model(self):
        base_dir = Path(__file__).resolve().parent
        final_model_path = base_dir / self.model_info.artifact
        
        if not final_model_path.exists():
            raise FileNotFoundError(f"Model not found at {final_model_path}")
        
        # Initialize session
        self.session = ort.InferenceSession(str(final_model_path), providers=['CPUExecutionProvider'])
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
        
        # FIX: Check if model expects float16 or float32
        self.expected_dtype = self.session.get_inputs()[0].type
        print(f"Model expects: {self.expected_dtype}")

    def infer(self, jpeg_bytes): # type: ignore
        nparr = np.frombuffer(jpeg_bytes, np.uint8)
        self.orig_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if self.orig_img is None:
            raise ValueError("Could not decode image.")

        # Pre-processing (YOLOv5 ONNX expects NCHW)
        h, w = self.model_info.input_shape[:2]
        img_resized = cv2.resize(self.orig_img, (w, h))
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        
        # Convert HWC -> NCHW and Normalize
        input_data = img_rgb.transpose(2, 0, 1) 
        input_data = np.expand_dims(input_data, axis=0)
        
        # FIX: Cast to float16 if the model requires it
        if "float16" in self.expected_dtype:
            input_data = input_data.astype(np.float16) / 255.0
        else:
            input_data = input_data.astype(np.float32) / 255.0

        return self.session.run([self.output_name], {self.input_name: input_data})[0]

    def post_process(self, raw_output, labels, conf_threshold=0.25, iou_threshold=0.45):
        """Standard YOLOv5 Post-processing"""
        predictions = np.squeeze(raw_output)
        
        # If model was FP16, the raw output might need casting back to float32 for math
        if predictions.dtype == np.float16:
            predictions = predictions.astype(np.float32)

        orig_h, orig_w = self.orig_img.shape[:2]
        model_h, model_w = self.model_info.input_shape[:2]
        x_scale, y_scale = orig_w / model_w, orig_h / model_h

        boxes, confidences, class_ids = [], [], []

        for pred in predictions:
            # YOLOv5 logic: Confidence = Objectness (index 4) * Max Class Probability (index 5+)
            obj_conf = pred[4]
            if obj_conf > conf_threshold:
                class_scores = pred[5:]
                class_id = np.argmax(class_scores)
                final_conf = obj_conf * class_scores[class_id]
                
                if final_conf > conf_threshold:
                    cx, cy, w, h = pred[:4]
                    x = int((cx - w/2) * x_scale)
                    y = int((cy - h/2) * y_scale)
                    boxes.append([x, y, int(w * x_scale), int(h * y_scale)])
                    confidences.append(float(final_conf))
                    class_ids.append(int(class_id))

        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, iou_threshold)
        
        detections = []
        if len(indices) > 0:
            for i in indices.flatten():
                detections.append({
                    "label": 'Dog',
                    "box": boxes[i],
                    "confidence": confidences[i],
                    # "label": labels[class_ids[i]] if labels else f"ID {class_ids[i]}",
                })
        return detections

    def get_annotated_image(self, detections):
        """Returns base64 string of the image with boxes"""
        if self.orig_img is None: return None
        
        annotated = self.orig_img.copy()
        for det in detections:
            print(f'det: {det}')
            x, y, w, h = det["box"]
            label = f"{det['label']} {det['confidence']:.1%}"
            cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(annotated, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', annotated)
        return base64.b64encode(buffer).decode('utf-8')