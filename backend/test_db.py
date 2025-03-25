from infrastructure.dependencies.dependencies import engine
from sqlalchemy import text

with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print("Conexión exitosa:", result.scalar())