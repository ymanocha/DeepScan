from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from database.base import sessionLocal
from models.scan import Scan
from api.auth import get_current_user
from database.supabase_client import supabase

import os

router = APIRouter()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_history(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    scans = db.query(Scan).filter(Scan.user_email == current_user.email).order_by(Scan.created_at.desc()).all()
    return scans

@router.get("/{scan_id}")
def view_scan(
    scan_id:int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    scan = db.query(Scan).filter(Scan.id == scan_id, Scan.user_email==current_user.email).first()
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found")
    return scan

@router.delete("/{scan_id}")
def delete_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    scan = db.query(Scan).filter(
        Scan.id == scan_id, 
        Scan.user_email == current_user.email
    ).first()

    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    try:
        if scan.lime_image:
            lime_path = scan.lime_image.split("/storage/v1/object/public/scans")[-1]
            supabase.storage.from_("scans").remove([lime_path])
    except Exception as e:
        print(f"Supabase deletion error: {e}")

    db.delete(scan)
    db.commit()

    return {"message": "Scan deleted successfully"}



@router.get("/dashboard/data")
def get_dashboard(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    
    user_scans = db.query(Scan).filter(Scan.user_email == current_user.email)

    total = user_scans.count()
    fake_count = user_scans.filter(Scan.result == "FAKE").count()
    real_count = user_scans.filter(Scan.result == "REAL").count()

    avg_confidence = (
        db.query(func.avg(Scan.confidence))
        .filter(Scan.user_email == current_user.email)
        .scalar()
    )

    
    date_stats = (
        db.query(func.date(Scan.created_at), func.count(Scan.id))
        .filter(Scan.user_email == current_user.email)
        .group_by(func.date(Scan.created_at))
        .order_by(func.date(Scan.created_at))
        .all()
    )

    chart_data = [{"date": str(d), "count": c} for d, c in date_stats] #?

    return {
        "total": total,
        "fake": fake_count,
        "real": real_count,
        "avg_confidence": round(avg_confidence or 0, 2),
        "history": chart_data,
    }
