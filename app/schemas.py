from datetime import datetime
from pydantic import BaseModel, EmailStr


# =====================================================
# Authentication
# =====================================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# =====================================================
# Users
# =====================================================

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    is_admin: bool = False


class UserUpdate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    is_admin: bool = False


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


# =====================================================
# Fish Farms
# =====================================================

class FarmCreate(BaseModel):
    name: str
    location: str
    owner: str
    fish_type: str
    ponds: int
    status: str = "Healthy"


class FarmUpdate(BaseModel):
    name: str
    location: str
    owner: str
    fish_type: str
    ponds: int
    status: str


class FarmResponse(BaseModel):
    id: int
    name: str
    location: str
    owner: str
    fish_type: str
    ponds: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# =====================================================
# Investments
# =====================================================

class InvestmentCreate(BaseModel):
    investor_name: str
    farm_id: int
    amount: float
    status: str = "Pending"


class InvestmentUpdate(BaseModel):
    investor_name: str
    farm_id: int
    amount: float
    status: str


class InvestmentResponse(BaseModel):
    id: int
    investor_name: str
    farm_id: int
    farm_name: str | None = None
    amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# =====================================================
# Marketplace
# =====================================================

class MarketplaceCreate(BaseModel):
    product_name: str
    category: str
    price: float
    stock: int
    seller: str
    status: str = "Available"


class MarketplaceUpdate(BaseModel):
    product_name: str
    category: str
    price: float
    stock: int
    seller: str
    status: str


class MarketplaceResponse(BaseModel):
    id: int
    product_name: str
    category: str
    price: float
    stock: int
    seller: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# =====================================================
# Settings
# =====================================================

class SettingsUpdate(BaseModel):
    company_name: str
    company_email: EmailStr
    company_phone: str
    company_address: str
    currency: str
    theme: str

    email_notifications: bool = True
    ai_alerts: bool = True
    dark_mode: bool = False
    maintenance_mode: bool = False


class SettingsResponse(BaseModel):
    id: int

    company_name: str
    company_email: EmailStr
    company_phone: str
    company_address: str

    currency: str
    theme: str

    email_notifications: bool
    ai_alerts: bool
    dark_mode: bool
    maintenance_mode: bool

    created_at: datetime

    class Config:
        from_attributes = True


# =====================================================
# AI Assistant
# =====================================================

class AIRequest(BaseModel):
    question: str


class AIResponse(BaseModel):
    answer: str


class AIConversationResponse(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime

    class Config:
        from_attributes = True