from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import MarketplaceItem, User
from app.schemas import (
    MarketplaceCreate,
    MarketplaceUpdate,
    MarketplaceResponse,
)
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/marketplace",
    tags=["Marketplace"],
)


def admin_required(current_user: User):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required",
        )


# ==========================================
# Get all marketplace items
# ==========================================

@router.get("/", response_model=list[MarketplaceResponse])
def get_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    admin_required(current_user)

    return db.query(MarketplaceItem).all()


# ==========================================
# Create item
# ==========================================

@router.post(
    "/",
    response_model=MarketplaceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_item(
    item: MarketplaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    admin_required(current_user)

    new_item = MarketplaceItem(
        product_name=item.product_name,
        category=item.category,
        price=item.price,
        stock=item.stock,
        seller=item.seller,
        status=item.status,
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


# ==========================================
# Update item
# ==========================================

@router.put("/{item_id}", response_model=MarketplaceResponse)
def update_item(
    item_id: int,
    item: MarketplaceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    admin_required(current_user)

    existing = (
        db.query(MarketplaceItem)
        .filter(MarketplaceItem.id == item_id)
        .first()
    )

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail="Marketplace item not found",
        )

    existing.product_name = item.product_name
    existing.category = item.category
    existing.price = item.price
    existing.stock = item.stock
    existing.seller = item.seller
    existing.status = item.status

    db.commit()
    db.refresh(existing)

    return existing


# ==========================================
# Delete item
# ==========================================

@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    admin_required(current_user)

    item = (
        db.query(MarketplaceItem)
        .filter(MarketplaceItem.id == item_id)
        .first()
    )

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Marketplace item not found",
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Marketplace item deleted successfully"
    }