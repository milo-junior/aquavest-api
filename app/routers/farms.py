from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Farm
from app.schemas import FarmCreate, FarmResponse
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/farms",
    tags=["Farms"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================
# Get All Farms
# ==========================
@router.get("/", response_model=list[FarmResponse])
def get_farms(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(Farm).order_by(Farm.id.desc()).all()


# ==========================
# Create Farm
# ==========================
@router.post("/", response_model=FarmResponse)
def create_farm(
    farm: FarmCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_farm = Farm(
        name=farm.name,
        location=farm.location,
        owner=farm.owner,
        fish_type=farm.fish_type,
        ponds=farm.ponds,
        status=farm.status,
    )

    db.add(new_farm)
    db.commit()
    db.refresh(new_farm)

    return new_farm


# ==========================
# Update Farm
# ==========================
@router.put("/{farm_id}", response_model=FarmResponse)
def update_farm(
    farm_id: int,
    farm: FarmCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing = db.query(Farm).filter(Farm.id == farm_id).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Farm not found",
        )

    existing.name = farm.name
    existing.location = farm.location
    existing.owner = farm.owner
    existing.fish_type = farm.fish_type
    existing.ponds = farm.ponds
    existing.status = farm.status

    db.commit()
    db.refresh(existing)

    return existing


# ==========================
# Delete Farm
# ==========================
@router.delete("/{farm_id}")
def delete_farm(
    farm_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()

    if not farm:
        raise HTTPException(
            status_code=404,
            detail="Farm not found",
        )

    db.delete(farm)
    db.commit()

    return {
        "message": "Farm deleted successfully"
    }