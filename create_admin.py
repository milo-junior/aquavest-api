from app.database import SessionLocal
from app.models import User
from app.core.security import hash_password

db = SessionLocal()

existing = db.query(User).filter(
    User.email == "admin@aquavest.com"
).first()

if existing:
    print("Admin already exists.")
else:
    admin = User(
        full_name="System Administrator",
        email="admin@aquavest.com",
        password=hash_password("Admin123"),
        is_admin=True,
    )

    db.add(admin)
    db.commit()

    print("Admin created successfully.")
