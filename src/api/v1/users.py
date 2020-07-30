from typing import List
from fastapi import APIRouter
from fastapi import HTTPException
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from tortoise.contrib.fastapi import HTTPNotFoundError

import config
from db.models.base import Status
from db.models.users import User_Pydantic
from db.models.users import UserIn_Pydantic
from db.models.users import Users

user_router = APIRouter()

templates = Jinja2Templates(directory=f"{config.get_root()[1]}/html")


@user_router.get("/test")
async def read_item(request: Request, ):
    return templates.TemplateResponse("index.html", {"request": request})


@user_router.get("/", response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())


@user_router.post("/", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@user_router.get("/{user_id}",
                 response_model=User_Pydantic,
                 responses={404: {
                     "model": HTTPNotFoundError
                 }})
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@user_router.post("/{user_id}",
                  response_model=User_Pydantic,
                  responses={404: {
                      "model": HTTPNotFoundError
                  }})
async def update_user(user_id: int, user: UserIn_Pydantic):
    await Users.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@user_router.delete("/{user_id}",
                    response_model=Status,
                    responses={404: {
                        "model": HTTPNotFoundError
                    }})
async def delete_user(user_id: int):
    deleted_count = await Users.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404,
                            detail=f"User {user_id} not found")
    return Status(message=f"Deleted user {user_id}")
