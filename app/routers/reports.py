from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Farm, Investment
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


def admin_required(current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required",
        )


# ==========================================
# Dashboard Summary
# ==========================================

@router.get("/summary")
def reports_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    admin_required(current_user)

    total_users = db.query(User).count()
    total_farms = db.query(Farm).count()
    total_investments = db.query(Investment).count()

    investment_value = (
        db.query(func.sum(Investment.amount))
        .scalar()
        or 0
    )

    active = (
        db.query(Investment)
        .filter(Investment.status == "Active")
        .count()
    )

    pending = (
        db.query(Investment)
        .filter(Investment.status == "Pending")
        .count()
    )

    completed = (
        db.query(Investment)
        .filter(Investment.status == "Completed")
        .count()
    )

    healthy_farms = (
        db.query(Farm)
        .filter(Farm.status == "Healthy")
        .count()
    )

    unhealthy_farms = (
        db.query(Farm)
        .filter(Farm.status != "Healthy")
        .count()
    )

    return {
        "users": total_users,
        "farms": total_farms,
        "investments": total_investments,
        "investment_value": float(investment_value),

        "investment_status": {
            "active": active,
            "pending": pending,
            "completed": completed,
        },

        "farm_status": {
            "healthy": healthy_farms,
            "unhealthy": unhealthy_farms,
        },
    }


# ==========================================
# Fish Type Distribution
# ==========================================

@router.get("/fish-types")
def fish_type_distribution(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    admin_required(current_user)

    data = (
        db.query(
            Farm.fish_type,
            func.count(Farm.id)
        )
        .group_by(Farm.fish_type)
        .all()
    )

    return [
        {
            "fish_type": fish_type,
            "count": count,
        }
        for fish_type, count in data
    ]


# ==========================================
# Investment Status Distribution
# ==========================================

@router.get("/investment-status")
def investment_status_distribution(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    admin_required(current_user)

    data = (
        db.query(
            Investment.status,
            func.count(Investment.id)
        )
        .group_by(Investment.status)
        .all()
    )

    return [
        {
            "status": status,
            "count": count,
        }
        for status, count in data
    ]


# ==========================================
# Farm Status Distribution
# ==========================================

@router.get("/farm-status")
def farm_status_distribution(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    admin_required(current_user)

    data = (
        db.query(
            Farm.status,
            func.count(Farm.id)
        )
        .group_by(Farm.status)
        .all()
    )

    return [
        {
            "status": status,
            "count": count,
        }
        for status, count in data
    ]