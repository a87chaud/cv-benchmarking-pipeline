from ultralytics import YOLO
import numpy as np
import base64
import cv2
import imghdr
import os
import io

class YoloV5:
    def __init__(self):
        self.model = YOLO("yolov5nu.pt")
    
    def _run_yolo_image_inference(self, file_bytes):
        image_array = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if image_array is None:
            print(f"File bytes length is {len(file_bytes)}")
            raise ValueError("OpenCV failed to decode image bytes. Check if the input is a valid image file.")
        results = self.model.predict(source=image_array, verbose=False)
        annotated_image_bgr = results[0].plot()
        success, buffer = cv2.imencode('jpg', annotated_image_bgr)
        if not success:
            raise Exception("Could not encode image")
        jpg_bytes = buffer.tobytes()
        img_base64 = base64.encode(jpg_bytes).decode('utf-8')
        return {"image": img_base64, "speed": results[0].speed, "boxes": len(results[0].boxes)}
    
    def _run_yolo_video_inference(self, file_bytes):
        # Ensure debug directory exists
        DEBUG_DIR = "./debug"
        os.makedirs(DEBUG_DIR, exist_ok=True)

        # Input path
        input_path = os.path.join(DEBUG_DIR, "input_debug.mp4")

        # Output path
        output_path = os.path.join(DEBUG_DIR, "output_annotated_debug.mp4")

        # Write incoming bytes into file for debugging
        with open(input_path, "wb") as f:
            f.write(file_bytes)

        print(f"[DEBUG] Saved input video to: {input_path}")

        cap = cv2.VideoCapture(input_path)

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = self.model.predict(frame, verbose=False)
            annotated = results[0].plot()
            out.write(annotated)

        cap.release()
        out.release()

        print(f"[DEBUG] Saved annotated video to: {output_path}")

        # Encode output to base64
        with open(output_path, "rb") as f:
            video_base64 = base64.b64encode(f.read()).decode("utf-8")
        print("[DEBUG] Base64 length:", len(video_base64))
        return {
            "type": "video",
            "image": video_base64,
            "speed": 0,
            "boxes": 69
        }
    def run_yolo_inference(self, file):
        file.seek(0)
        file_bytes = np.frombuffer(file.read(), np.uint8)
        is_img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR) is not None
        if is_img:
            return self._run_yolo_image_inference(file_bytes)
        else:
            return self._run_yolo_video_inference(file_bytes)