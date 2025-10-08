from fastapi import APIRouter,UploadFile,File
from ml.predictor import EnsembleDeepfakeDetector

router = APIRouter()

detector = EnsembleDeepfakeDetector("Model/resnet50_model_ep10.keras", "Model/resnet50_model_ep10(2).keras" , demo_mode=True)

@router.post("/detect")
async def detect(file: UploadFile = File(...)):
    temp_path = f"temp_videos/{file.filename}"
    with open(temp_path,"wb") as f:
        f.write(await file.read())
   
    result = detector.predict_video(temp_path, explain=True)
    return result