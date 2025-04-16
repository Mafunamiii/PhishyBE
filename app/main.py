from fastapi import FastAPI
from app.modules.user.routes.routes import router as user_router
from app.utils.logger import get_logger
from app.core.database import init_db

logger = get_logger("main")
app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()  # Ensure tables exist on startup

app.include_router(user_router)
