import cv2
import numpy as np

class PreProcess:
    '''
    Class to handle the pre-processing of the image/video
    We will allow users to input a pipeline of pre-processing they want done
    But to start we will run the image through some basic pre-processing depending on the use case
    '''
    def __init__(self, use_case: str):
        self.use_case = use_case
    
    def resize(self, image, size=(224, 224)):
        return cv2.resize(image, size)
    
    def normalize(self, image):
        return image / 255.0
    
    def grayscale(self,image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    def blur(self, image, ksize=(5,5)):
        return cv2.GaussianBlur(image, ksize, 0)
    def execute_pipeline(self,image):
        '''
        Given the use case run the right pipeline
        '''
        img1 = self.resize(image)
        # img2 = self.grayscale(img1)
        return self.normalize(img1)

    