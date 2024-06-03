from .database import AsyncSessionLocal


def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
