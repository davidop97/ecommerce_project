# create_tables.py
from core.domain.models import Base
from infrastructure.dependencies.dependencies import engine

Base.metadata.create_all(bind=engine)