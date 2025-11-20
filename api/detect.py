from fastapi import APIRouter, UploadFile, File, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
import os, shutil, pathlib, uuid

from ml.predictor import EnsembleDeepfakeDetector
from database.base import sessionLocal
from database.supabase_client import supabase
from models.scan import Scan
from api.auth import SECRET_KEY, ALGORITHM

router = APIRouter()

detector = EnsembleDeepfakeDetector(
    "Model/efficientnet_modelB7.keras",
    demo_mode=True
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
async def detect(
    file: UploadFile = File(...),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    temp_path = f"temp_videos/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    result = detector.predict_video(temp_path, explain=True)
    print(" MODEL OUTPUT:", result)

    result_label = result.get("final_label") or result.get("label")
    confidence_raw = result.get("confidence_score")
    lime_path = result.get("lime_explanation_path")

    try:
        confidence = float(str(confidence_raw).replace("%", "").strip())
    except Exception:
        confidence = 0.0

    user_email = None
    if authorization:
        try:
            token = authorization.split("Bearer ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_email = payload.get("sub")
            print("USER:", user_email)
        except (JWTError, IndexError):
            print("Invalid token format or decode error")

    lime_url = None

   
    if user_email:
        try:
            if lime_path and os.path.exists(lime_path):
                lime_path = str(pathlib.Path(lime_path).resolve())
                unique_id = uuid.uuid4().hex[:8]

                new_lime_path = f"temp_videos/{unique_id}_{file.filename}_lime.png"
                shutil.copy(lime_path, new_lime_path)
                lime_path = new_lime_path

                with open(lime_path, "rb") as lime_file:
                    supabase.storage.from_("scans").upload(
                        f"lime/{unique_id}_{file.filename}_lime.png",
                        lime_file.read(),
                        {"content-type": "image/png"},
                       
                    )
                lime_url = f"{os.getenv('SUPABASE_URL')}/storage/v1/object/public/scans/lime/{unique_id}_{file.filename}_lime.png"

     
            new_scan = Scan(
                user_email=user_email,
                video_name=file.filename,
                result=result_label,
                confidence=confidence,
                lime_image=lime_url
            )
            db.add(new_scan)
            db.commit()
            db.refresh(new_scan)
            print(" Scan saved to DB")

        except Exception as e:
            print(" Upload or DB error:", e)
            raise HTTPException(status_code=500, detail=f"Error saving scan: {str(e)}")
    else:
        if lime_path and os.path.exists(lime_path):
             new_name = f"{uuid.uuid4().hex}.png"
             public_path = f"temp_lime/{new_name}"
             shutil.copy(lime_path, public_path)

             lime_url = f"/temp_lime/{new_name}"

    return {
        "result": result_label,
        "confidence": confidence,
        "lime_image": lime_url,
        "saved": bool(user_email)
    }
