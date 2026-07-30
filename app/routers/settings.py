from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Setting, User
from app.schemas import (
    SettingsUpdate,
    SettingsResponse,
)
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)


# =====================================================
# Admin Permission
# =====================================================

def admin_required(current_user: User):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required",
        )


# =====================================================
# Get Settings
# =====================================================

@router.get("/", response_model=SettingsResponse)
def get_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    settings = db.query(Setting).first()

    if settings is None:
        settings = Setting()

        db.add(settings)
        db.commit()
        db.refresh(settings)

    return settings


# =====================================================
# Update Settings
# =====================================================

@router.put("/", response_model=SettingsResponse)
def update_settings(
    payload: SettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    admin_required(current_user)

    settings = db.query(Setting).first()

    if settings is None:
        settings = Setting()
        db.add(settings)
        db.commit()
        db.refresh(settings)

    settings.company_name = payload.company_name
    settings.company_email = payload.company_email
    settings.company_phone = payload.company_phone
    settings.company_address = payload.company_address

    settings.currency = payload.currency
    settings.theme = payload.theme

    settings.email_notifications = payload.email_notifications
    settings.ai_alerts = payload.ai_alerts
    settings.dark_mode = payload.dark_mode
    settings.maintenance_mode = payload.maintenance_mode

    db.commit()
    db.refresh(settings)

    return settings