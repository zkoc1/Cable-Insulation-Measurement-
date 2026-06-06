from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
import os
import uuid
import shutil
import cv2
from core.models import MeasurementResult
from vision.three_core_analyzer import ThreeCoreAnalyzer
from vision.single_core_analyzer import SingleCoreAnalyzer
from vision.multi_stranded_analyzer import MultiStrandedAnalyzer

router = APIRouter()

UPLOAD_DIR = "uploads"
RESULTS_DIR = "static/results"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

@router.post("/measure", response_model=MeasurementResult)
async def measure_cable(
    file: UploadFile = File(...),
    cable_type: str = Form(...),
    pixel_to_mm: float = Form(...)
):
    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    input_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
    
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    if cable_type == "single":
        analyzer = SingleCoreAnalyzer(pixel_to_mm=pixel_to_mm)
    elif cable_type == "multi_stranded":
        analyzer = MultiStrandedAnalyzer(pixel_to_mm=pixel_to_mm)
    else:
        analyzer = ThreeCoreAnalyzer(pixel_to_mm=pixel_to_mm)
        
    try:
        results = analyzer.analyze(input_path)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
        
    result_img_filename = f"{file_id}_result.jpg"
    result_img_path = os.path.join(RESULTS_DIR, result_img_filename)
    cv2.imwrite(result_img_path, results["result_image"])
    
    return MeasurementResult(
        image_name=file.filename,
        pixel_to_mm=pixel_to_mm,
        measurement_count=len(results["thickness_measurements_mm"]),
        outer_center_px=results["outer_center_px"],
        inner_center_px=results["inner_center_px"],
        outer_diameter_px=results["outer_diameter_px"],
        inner_diameter_px=results["inner_diameter_px"],
        outer_diameter_mm=results["outer_diameter_mm"],
        inner_diameter_mm=results["inner_diameter_mm"],
        thickness_measurements_mm=results["thickness_measurements_mm"],
        min_thickness_mm=results["min_thickness_mm"],
        max_thickness_mm=results["max_thickness_mm"],
        mean_thickness_mm=results["mean_thickness_mm"],
        eccentricity_mm=results["eccentricity_mm"],
        result_image_url=f"/results/{result_img_filename}"
    )
