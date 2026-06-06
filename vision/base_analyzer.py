from abc import ABC, abstractmethod
import cv2
import numpy as np

class BaseCableAnalyzer(ABC):
    def __init__(self, pixel_to_mm: float):
        self.pixel_to_mm = pixel_to_mm

    @abstractmethod
    def analyze(self, image_path: str):
        pass

    def calculate_distance(self, pt1, pt2):
        return np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
