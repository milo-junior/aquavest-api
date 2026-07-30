from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Investment, Farm, User
from app.schemas import (
    InvestmentCreate,
    InvestmentUpdate,
    InvestmentResponse,
)
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/investments",
    tags=["Investments"],
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
# Get All Investments
# =====================================================

@router.get("/", response_model=list[InvestmentResponse])
def get_investments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    admin_required(current_user)

    investments = db.query(Investment).all()

    return [
        InvestmentResponse(
            id=i.id,
            investor_name=i.investor_name,
            farm_id=i.farm_id,
            farm_name=i.farm.name if i.farm else None,
            amount=i.amount,
            status=i.status,
            created_at=i.created_at,
        )
        for i in investments
    ]


# =====================================================
# Create Investment
# =====================================================

@router.post("/", response_model=InvestmentResponse, status_code=status.HTTP_201_CREATED)
def create_investment(
    investment: InvestmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    admin_required(current_user)

    farm = db.query(Farm).filter(Farm.id == investment.farm_id).first()

    if not farm:
        raise HTTPException(
            status_code=404,
            detail="Farm not found",
        )

    new_investment = Investment(
        investor_name=investment.investor_name,
        farm_id=investment.farm_id,
        amount=investment.amount,
        status=investment.status,
    )

    db.add(new_investment)
    db.commit()
    db.refresh(new_investment)

    return InvestmentResponse(
        id=new_investment.id,
        investor_name=new_investment.investor_name,
        farm_id=new_investment.farm_id,
        farm_name=farm.name,
        amount=new_investment.amount,
        status=new_investment.status,
        created_at=new_investment.created_at,
    )


# =====================================================
# Update Investment
# =====================================================

@router.put("/{investment_id}", response_model=InvestmentResponse)
def update_investment(
    investment_id: int,
    investment: InvestmentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    admin_required(current_user)

    existing = db.query(Investment).filter(
        Investment.id == investment_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Investment not found",
        )

    farm = db.query(Farm).filter(
        Farm.id == investment.farm_id
    ).first()

    if not farm:
        raise HTTPException(
            status_code=404,
            detail="Farm not found",
        )

    existing.investor_name = investment.investor_name
    existing.farm_id = investment.farm_id
    existing.amount = investment.amount
    existing.status = investment.status

    db.commit()
    db.refresh(existing)

    return InvestmentResponse(
        id=existing.id,
        investor_name=existing.investor_name,
        farm_id=existing.farm_id,
        farm_name=farm.name,
        amount=existing.amount,
        status=existing.status,
        created_at=existing.created_at,
    )


# =====================================================
# Delete Investment
# =====================================================

@router.delete("/{investment_id}")
def delete_investment(
    investment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    admin_required(current_user)

    investment = db.query(Investment).filter(
        Investment.id == investment_id
    ).first()

    if not investment:
        raise HTTPException(
            status_code=404,
            detail="Investment not found",
        )

    db.delete(investment)
    db.commit()

    return {
        "message": "Investment deleted successfully"
    }