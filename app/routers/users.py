from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate
from app.core.security import hash_password
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def admin_required(current_user: User):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required",
        )


# ----------------------------
# Get all users
# ----------------------------
@router.get("/")
def get_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    admin_required(current_user)

    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "is_admin": user.is_admin,
        }
        for user in users
    ]


# ----------------------------
# Create user
# ----------------------------
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    admin_required(current_user)

    existing = db.query(User).filter(User.email == user.email).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password),
        is_admin=user.is_admin,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "full_name": new_user.full_name,
            "email": new_user.email,
            "is_admin": new_user.is_admin,
        },
    }


# ----------------------------
# Update user
# ----------------------------
@router.put("/{user_id}")
def update_user(
    user_id: int,
    user: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    admin_required(current_user)

    existing = db.query(User).filter(User.id == user_id).first()

    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    duplicate = (
        db.query(User)
        .filter(User.email == user.email, User.id != user_id)
        .first()
    )

    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    existing.full_name = user.full_name
    existing.email = user.email
    existing.password = hash_password(user.password)
    existing.is_admin = user.is_admin

    db.commit()
    db.refresh(existing)

    return {
        "message": "User updated successfully",
        "user": {
            "id": existing.id,
            "full_name": existing.full_name,
            "email": existing.email,
            "is_admin": existing.is_admin,
        },
    }


# ----------------------------
# Delete user
# ----------------------------
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    admin_required(current_user)

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }