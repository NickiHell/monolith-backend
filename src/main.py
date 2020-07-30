# https://github.com/tiangolo/fastapi/issues/386

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

import config
from api.v1.api import api_router

app = FastAPI(title='Monolith')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    db_url=config.DB_URL,
    modules={"models": ["db.models.users"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

# config.get_root()
app.mount("/static", StaticFiles(directory=config.get_root()[1]), name="static")
app.include_router(api_router, prefix='/v1')
