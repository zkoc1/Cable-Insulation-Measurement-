import cv2
import numpy as np
import math
from .base_analyzer import BaseCableAnalyzer

class MultiStrandedAnalyzer(BaseCableAnalyzer):
    def analyze(self, image_path: str):
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Goruntu okunamadi.")
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            raise ValueError("Kontur bulunamadi.")
            
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        outer_contour = contours[0]
        
        (ox, oy), outer_radius = cv2.minEnclosingCircle(outer_contour)
        outer_center = (int(ox), int(oy))
        outer_diameter_px = outer_radius * 2
        
        inner_contours = []
        for c in contours[1:]:
            area = cv2.contourArea(c)
            # Cok telli kabloda ufak teller ayri kontur olabilir, esigi dusuruyoruz
            if area > (cv2.contourArea(outer_contour) * 0.005):
                inner_contours.append(c)
                
        if len(inner_contours) == 0:
            raise ValueError("Ic damar telleri bulunamadi.")
            
        # Tum ic konturlari (telleri) tek bir butun olarak sarmaliyoruz
        all_inner_pts = np.vstack(inner_contours)
        (ix, iy), inner_radius = cv2.minEnclosingCircle(all_inner_pts)
        inner_center = (int(ix), int(iy))
        inner_diameter_px = inner_radius * 2
        
        # Check if it's actually a 3-core
        if len(inner_contours) == 3:
             # Eger tam 3 tane esit boyutta kontur varsa, bu muhtemelen 3 deliklidir.
             c1, c2, c3 = inner_contours[0], inner_contours[1], inner_contours[2]
             ratio1 = cv2.contourArea(c1) / cv2.contourArea(outer_contour)
             if ratio1 < 0.2: 
                 # 3 delikli oldugu bariz
                 raise ValueError("Kablo tipi uyusmazligi: Goruntude cok damarli yapi tespit edildi ancak 'Tek Damarli (Cok Telli)' secenegi isaretlendi. Lutfen kablo tipini dogru secin.")
                 
        eccentricity_px = self.calculate_distance(outer_center, inner_center)
        
        thickness_measurements_px = []
        angles = [i * 60 for i in range(6)]
        for angle in angles:
            rad = math.radians(angle)
            p1 = (int(outer_center[0] + outer_radius * math.cos(rad)), 
                  int(outer_center[1] + outer_radius * math.sin(rad)))
            p2 = (int(inner_center[0] + inner_radius * math.cos(rad)), 
                  int(inner_center[1] + inner_radius * math.sin(rad)))
            dist = self.calculate_distance(p1, p2)
            thickness_measurements_px.append(abs(dist))
            
        min_thick = min(thickness_measurements_px)
        max_thick = max(thickness_measurements_px)
        mean_thick = sum(thickness_measurements_px) / len(thickness_measurements_px)
        
        cv2.circle(img, outer_center, int(outer_radius), (255, 0, 0), 2)
        cv2.circle(img, inner_center, int(inner_radius), (0, 255, 0), 2)
        cv2.drawMarker(img, outer_center, (255, 0, 0), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)
        cv2.drawMarker(img, inner_center, (0, 255, 0), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)
        
        for angle, dist in zip(angles, thickness_measurements_px):
            rad = math.radians(angle)
            p1 = (int(outer_center[0] + outer_radius * math.cos(rad)), 
                  int(outer_center[1] + outer_radius * math.sin(rad)))
            p2 = (int(outer_center[0] + (outer_radius - dist) * math.cos(rad)), 
                  int(outer_center[1] + (outer_radius - dist) * math.sin(rad)))
            cv2.line(img, p1, p2, (0, 0, 255), 2)
            
        return {
            "outer_center_px": outer_center,
            "inner_center_px": inner_center,
            "outer_diameter_px": outer_diameter_px,
            "inner_diameter_px": inner_diameter_px,
            "outer_diameter_mm": outer_diameter_px * self.pixel_to_mm,
            "inner_diameter_mm": inner_diameter_px * self.pixel_to_mm,
            "thickness_measurements_mm": [t * self.pixel_to_mm for t in thickness_measurements_px],
            "min_thickness_mm": min_thick * self.pixel_to_mm,
            "max_thickness_mm": max_thick * self.pixel_to_mm,
            "mean_thickness_mm": mean_thick * self.pixel_to_mm,
            "eccentricity_mm": eccentricity_px * self.pixel_to_mm,
            "result_image": img
        }
