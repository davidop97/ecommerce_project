# routes/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from infrastructure.dependencies.dependencies import get_db, get_auth_service, get_user_repo
from core.domain.services import AuthService
from core.domain.repositories import UserRepository
from infrastructure.adapters.contracts.contracts import TokenResponse
from core.domain.models import User
from jose import jwt, JWTError
from decouple import config

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY: str = config('SECRET_KEY')
ALGORITHM: str = config('ALGORITHM')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    user_repo: UserRepository = Depends(get_user_repo)  
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("SECRET_KEY en validación:", SECRET_KEY)  # Se añade aquí
    print("Token recibido:", token)  # Para ver el token que llega
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as e:
        print("JWTError:", str(e))
        raise credentials_exception
    user = user_repo.get_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user

@router.post("/token", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(data={"sub": user.email})
    return TokenResponse(access_token=access_token, token_type="bearer")