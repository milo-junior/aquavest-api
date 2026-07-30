from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import (
    User,
    Farm,
    Investment,
    MarketplaceItem,
    AIConversation,
)
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/stats")
def dashboard_stats(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    users = db.query(func.count(User.id)).scalar()

    farms = db.query(func.count(Farm.id)).scalar()

    investments = db.query(func.count(Investment.id)).scalar()

    investment_amount = (
        db.query(func.sum(Investment.amount)).scalar() or 0
    )

    products = db.query(func.count(MarketplaceItem.id)).scalar()

    ai_chats = db.query(func.count(AIConversation.id)).scalar()

    return {
        "users": users,
        "farms": farms,
        "investments": investments,
        "investment_amount": investment_amount,
        "products": products,
        "ai_chats": ai_chats,
    }