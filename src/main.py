from fastapi import FastAPI

from .accounts import router
from .database import engine, Base
from .auth import router

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


app.include_router(router.router)
app.include_router(router.router)
