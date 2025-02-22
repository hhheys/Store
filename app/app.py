from fastapi import FastAPI
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.admin.routes import router
from app.routes import setup_routes
from app.store.database import lifespan

app = FastAPI(lifespan=lifespan)

setup_routes(app)

app.mount("/static", StaticFiles(directory="../static"), name="static")