from pathlib import Path
import cv2
import numpy as np
import tensorflow as tf
from app.models.base_model import BaseModel

class TfLiteModel(BaseModel):
    def __init__(self, model_info):
        super().__init__(model_info=model_info)
        self.load_model()
        self.orig_w = None
        self.orig_h = None

    def load_model(self):
        base_dir = Path(__file__).resolve().parent
        final_model_path = base_dir / self.model_info.artifact

        if not final_model_path.exists():
            raise FileNotFoundError(f"Model not found at {final_model_path}")
        self.interpreter = tf.lite.Interpreter(model_path=str(final_model_path))
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
    
    def infer(self, jpeg_bytes):
            nparr = np.frombuffer(jpeg_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                raise ValueError("Could not decode image bytes.")

            self.orig_h, self.orig_w = img.shape[:2]

            # 2. Pre-processing
            input_shape = self.input_details[0]['shape'] 
            h, w = input_shape[1], input_shape[2]
            
            img_resized = cv2.resize(img, (w, h))
            img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
            input_data = np.expand_dims(img_rgb, axis=0)

            # 3. DYNAMIC TYPE CHECKING (The Fix)
            input_dtype = self.input_details[0]['dtype']
            
            if input_dtype == np.uint8:
                # For Quantized models: Keep as 0-255, just ensure type is uint8
                input_data = input_data.astype(np.uint8)
            else:
                # For Standard models: Normalize to 0.0 - 1.0
                input_data = input_data.astype(np.float32) / 255.0
            
            # 4. Run Inference
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            
            return self.interpreter.get_tensor(self.output_details[0]['index'])

    def post_process(self, raw_output, conf_threshold=0.25, iou_threshold=0.45):
        """Unified entry point for post-processing"""
        if self.model_info.task == "classification":
            return self._post_process_classification(raw_output)
        elif self.model_info.task == "Detection":
            return self._post_process_detection(raw_output, conf_threshold, iou_threshold)
        else:
            raise ValueError(f"Unsupported task: {self.model_info.task}")

    def _post_process_classification(self, raw_output):
        scores = np.squeeze(raw_output)
        class_id = np.argmax(scores)
        return {
            "type": "classification",
            "class_id": int(class_id),
            "confidence": float(scores[class_id])
        }

    def _post_process_detection(self, raw_output, conf_threshold, iou_threshold):
        print(f'raw output: {raw_output}')
        predictions = np.squeeze(raw_output).T 
        
        # Calculate scaling factors
        input_shape = self.input_details[0]['shape']
        model_h, model_w = input_shape[1], input_shape[2]
        
        x_scale = self.orig_w / model_w
        y_scale = self.orig_h / model_h

        boxes, confidences, class_ids = [], [], []

        for pred in predictions:
            print(f'preds: {pred}')
            score = np.max(pred[4:])
            if score > conf_threshold:
                cx, cy, w, h = pred[:4]
                
                # Scale coordinates back to original image size
                # And convert from center-xy to top-left-xy
                x = int((cx - w/2) * x_scale)
                y = int((cy - h/2) * y_scale)
                width = int(w * x_scale)
                height = int(h * y_scale)
                
                boxes.append([x, y, width, height])
                confidences.append(float(score))
                class_ids.append(int(np.argmax(pred[4:])))

        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, iou_threshold)
        
        detections = []
        if len(indices) > 0:
            for i in indices.flatten(): # type: ignore
                detections.append({
                    "box": boxes[i], # These are now in original pixel coordinates!
                    "confidence": confidences[i],
                    "class_id": class_ids[i]
                })
        
        return {"type": "detection", "results": detections}