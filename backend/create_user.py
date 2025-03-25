# create_user.py
from sqlalchemy.orm import Session
from infrastructure.dependencies.dependencies import get_db
from core.services.auth_service import AuthServiceImpl
from infrastructure.adapters.repositories.repositories import SQLUserRepository
from core.domain.models import User

db: Session = next(get_db())
auth_service = AuthServiceImpl(SQLUserRepository())
hashed_password = auth_service.get_password_hash("password1234")
user = User(email="test1@example.com", password=hashed_password, name="Test User 2")
db.add(user)
db.commit()
print("Usuario creado:", user.email)