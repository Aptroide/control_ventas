from fastapi import status, APIRouter, HTTPException, Depends
from .. import schemas, utils, oauth2
from ..database import execute_query


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# -------- Users --------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(new_user: schemas.User, user_id: int = Depends(oauth2.get_current_user)):

    new_user.password = utils.hash(new_user.password)

    query = """
    INSERT INTO minimarket.users (username, password) 
    VALUES (%s, %s) RETURNING id_user, username;
    """
    user_id = execute_query(query, 
                            (new_user.username, new_user.password), 
                            fetch="one")
    if "duplicate key value violates unique constraint" in str(user_id):
        raise HTTPException(status_code=409, detail="Duplicate entry: the product with the provided username already exists.")
    
    return user_id

@router.get("/{id_user}", response_model=schemas.UserOut)
def get_user_by_id(id_user: int, user_id: int = Depends(oauth2.get_current_user)):
    query = "SELECT id_user, username, created_at FROM minimarket.users WHERE id_user = %s"
    user = execute_query(query, 
                            (id_user, ), 
                            fetch="one")
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id_user} not found")
    return user