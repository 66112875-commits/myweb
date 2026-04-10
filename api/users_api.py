from fastapi import APIRouter
from fastapi.exceptions import HTTPException

router = APIRouter()

ENDPOINT = '/api/v1'


@router.get("/users")
async def users_list():
    return {"users": "List of users"}


@router.get(ENDPOINT + "/users")
async def users_get(id:int):
    if not id:
        raise HTTPException(
            status_code = 400, #Bad Request
            detail = "Invalid id!"
        )

    if not id in [1,2,3]:
                raise HTTPException(
            status_code = 404, #Not Found
            detail = "ID not found!"
        )

    try:
        div = id - id
        x = 10 / div

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong, Contact admin'
        )

    return {"users": f"get users by id {id}"}


@router.delete(ENDPOINT + "/users")
async def users_delete(id:int):
    return {"users": f"List of users {id}"}


@router.put(ENDPOINT + "/users")
async def users_put(id:int):
    return {"users": f"Update users by id {id}"}


@router.patch(ENDPOINT + "/users")
async def users_patch(id:int):
    return {"users": f"Update users patched by id {id}"}
