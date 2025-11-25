from ultralytics import YOLO
import numpy as np
import base64
import cv2
class YoloV5:
    def __init__(self):
        self.model = YOLO("yolov5nu.pt")
    def run_yolo_inference(self, img_file):
        img_file.seek(0)
        file_bytes = np.frombuffer(img_file.read(), np.uint8)
        # 2. Decode the image using OpenCV
        # # This results in a NumPy array with shape (H, W, C) and dtype np.uint8
        image_array = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR) 
        # --- CRITICAL CHECK ---
        # # Ensure the decoding was successful and the array is valid
        if image_array is None:
            print(f"DEBUG: File bytes length is {len(file_bytes)}")
            raise ValueError("OpenCV failed to decode image bytes. Check if the input is a valid image file.")

        results = self.model.predict(source=image_array, verbose=False)
        annotated_image_bgr = results[0].plot()
        success, buffer = cv2.imencode('.jpg', annotated_image_bgr)
        if not success:
            raise Exception("Could not encode annotated image to JPEG.")
        jpg_bytes = buffer.tobytes()
        # 5. Base64 Encode the Bytes
        img_base64 = base64.b64encode(jpg_bytes).decode('utf-8')
        # Return the Base64 string for the frontend
        return {"image": img_base64, "speed": results[0].speed, "boxes": 10}