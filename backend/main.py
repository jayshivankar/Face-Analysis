from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import numpy as np
import cv2
from PIL import Image
import io
import base64
import logging

from models.model_loader import ModelLoader
from services.face_analysis import FaceAnalysisService
from services.health_index import HealthIndexCalculator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Face Health Analyzer API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader = ModelLoader()
face_service = FaceAnalysisService(model_loader)
health_calculator = HealthIndexCalculator()


class Base64ImageRequest(BaseModel):
    image: str
    skin_image: Optional[str] = None


class AnalysisResponse(BaseModel):
    age: int
    gender: str
    fatigue: str
    emotion: str
    symmetry: dict
    skin_condition: Optional[str] = None
    health_index: dict
    confidence_scores: dict
    recommendations: List[str]


@app.get("/")
async def root():
    return {"message": "Face Health Analyzer API", "version": "2.0.0"}


@app.get("/health")
async def health_check():
    model_status = model_loader.get_model_status()
    return {
        "status": "healthy",
        "models": model_status
    }


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_face(
    face_image: UploadFile = File(...),
    skin_image: Optional[UploadFile] = File(None)
):
    try:
        face_img_data = await face_image.read()
        face_img = Image.open(io.BytesIO(face_img_data)).convert("RGB")
        face_array = np.array(face_img)

        skin_array = None
        if skin_image:
            skin_img_data = await skin_image.read()
            skin_img = Image.open(io.BytesIO(skin_img_data)).convert("RGB")
            skin_array = np.array(skin_img)

        result = face_service.analyze_complete(face_array, skin_array)

        health_index = health_calculator.calculate_health_index(result)
        result["health_index"] = health_index

        recommendations = health_calculator.generate_recommendations(result)
        result["recommendations"] = recommendations

        return result

    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/analyze/base64", response_model=AnalysisResponse)
async def analyze_face_base64(request: Base64ImageRequest):
    try:
        face_img_data = base64.b64decode(request.image.split(',')[1] if ',' in request.image else request.image)
        face_img = Image.open(io.BytesIO(face_img_data)).convert("RGB")
        face_array = np.array(face_img)

        skin_array = None
        if request.skin_image:
            skin_img_data = base64.b64decode(request.skin_image.split(',')[1] if ',' in request.skin_image else request.skin_image)
            skin_img = Image.open(io.BytesIO(skin_img_data)).convert("RGB")
            skin_array = np.array(skin_img)

        result = face_service.analyze_complete(face_array, skin_array)

        health_index = health_calculator.calculate_health_index(result)
        result["health_index"] = health_index

        recommendations = health_calculator.generate_recommendations(result)
        result["recommendations"] = recommendations

        return result

    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/analyze/age-gender")
async def analyze_age_gender(image: UploadFile = File(...)):
    try:
        img_data = await image.read()
        img = Image.open(io.BytesIO(img_data)).convert("RGB")
        img_array = np.array(img)

        result = face_service.analyze_age_gender(img_array)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/fatigue")
async def analyze_fatigue(image: UploadFile = File(...)):
    try:
        img_data = await image.read()
        img = Image.open(io.BytesIO(img_data)).convert("RGB")
        img_array = np.array(img)

        result = face_service.analyze_fatigue(img_array)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/symmetry")
async def analyze_symmetry(image: UploadFile = File(...)):
    try:
        img_data = await image.read()
        img = Image.open(io.BytesIO(img_data)).convert("RGB")
        img_array = np.array(img)

        result = face_service.analyze_symmetry(img_array)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/skin")
async def analyze_skin(image: UploadFile = File(...)):
    try:
        img_data = await image.read()
        img = Image.open(io.BytesIO(img_data)).convert("RGB")
        img_array = np.array(img)

        result = face_service.analyze_skin(img_array)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/emotion")
async def analyze_emotion(image: UploadFile = File(...)):
    try:
        img_data = await image.read()
        img = Image.open(io.BytesIO(img_data)).convert("RGB")
        img_array = np.array(img)

        result = face_service.analyze_emotion(img_array)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
