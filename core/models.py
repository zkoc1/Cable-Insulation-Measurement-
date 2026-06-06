from pydantic import BaseModel
from typing import List, Tuple

class MeasurementResult(BaseModel):
    image_name: str
    pixel_to_mm: float
    measurement_count: int
    outer_center_px: Tuple[int, int]
    inner_center_px: Tuple[int, int]
    outer_diameter_px: float
    inner_diameter_px: float
    outer_diameter_mm: float
    inner_diameter_mm: float
    thickness_measurements_mm: List[float]
    min_thickness_mm: float
    max_thickness_mm: float
    mean_thickness_mm: float
    eccentricity_mm: float
    result_image_url: str
