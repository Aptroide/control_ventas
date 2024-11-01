from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..database import execute_query
from .. import schemas, utils, oauth2

router = APIRouter(
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    
    query = "SELECT * FROM minimarket.users WHERE username = %s"
    user = execute_query(query, (user_credentials.username,), fetch="one")
    if not user:
        raise HTTPException(status_code=404, detail="Invalid username or password")
    
    if not utils.verify(user_credentials.password, user["password"]):
        raise HTTPException(status_code=404, detail="Invalid username or password")
    
    # Generate JWT token
    access_token = oauth2.create_access_token(data={"user_id": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}