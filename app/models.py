from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    ForeignKey,
    DateTime,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base


# =====================================================
# Users
# =====================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    password = Column(String, nullable=False)

    is_admin = Column(
        Boolean,
        default=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )


# =====================================================
# Fish Farms
# =====================================================

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    location = Column(String, nullable=False)

    owner = Column(String, nullable=False)

    fish_type = Column(String, nullable=False)

    ponds = Column(
        Integer,
        default=1,
    )

    status = Column(
        String,
        default="Healthy",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    investments = relationship(
        "Investment",
        back_populates="farm",
        cascade="all, delete-orphan",
    )


# =====================================================
# Investments
# =====================================================

class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)

    investor_name = Column(
        String,
        nullable=False,
    )

    farm_id = Column(
        Integer,
        ForeignKey("farms.id", ondelete="CASCADE"),
        nullable=False,
    )

    amount = Column(
        Float,
        nullable=False,
    )

    status = Column(
        String,
        default="Pending",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    farm = relationship(
        "Farm",
        back_populates="investments",
    )


# =====================================================
# Marketplace
# =====================================================

class MarketplaceItem(Base):
    __tablename__ = "marketplace"

    id = Column(Integer, primary_key=True, index=True)

    product_name = Column(
        String,
        nullable=False,
    )

    category = Column(
        String,
        nullable=False,
    )

    price = Column(
        Float,
        nullable=False,
    )

    stock = Column(
        Integer,
        default=0,
    )

    seller = Column(
        String,
        nullable=False,
    )

    status = Column(
        String,
        default="Available",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )


# =====================================================
# System Settings
# =====================================================

class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)

    company_name = Column(
        String,
        default="AquaVest",
    )

    company_email = Column(
        String,
        default="admin@aquavest.com",
    )

    company_phone = Column(
        String,
        default="",
    )

    company_address = Column(
        String,
        default="",
    )

    currency = Column(
        String,
        default="KES",
    )

    theme = Column(
        String,
        default="Light",
    )

    # Settings switches
    email_notifications = Column(
        Boolean,
        default=True,
    )

    ai_alerts = Column(
        Boolean,
        default=True,
    )

    dark_mode = Column(
        Boolean,
        default=False,
    )

    maintenance_mode = Column(
        Boolean,
        default=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )


# =====================================================
# AI Conversations
# =====================================================

class AIConversation(Base):
    __tablename__ = "ai_conversations"

    id = Column(Integer, primary_key=True, index=True)

    question = Column(
        Text,
        nullable=False,
    )

    answer = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )