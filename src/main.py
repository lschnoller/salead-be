from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import init_models
from .auth.router import router as auth_router
from .accounts.router import router as accounts_router
from .contacts.router import router as contacts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield
    # FUTURE: Add code to run on shutdown


app = FastAPI(lifespan=lifespan)


@app.on_event("startup")
async def on_startup():
    await init_models()


@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(contacts_router)
