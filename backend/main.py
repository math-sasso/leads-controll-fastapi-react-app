import fastapi
import crud
import sqlalchemy.orm as orm
import models

import schemas
from typing import List

from fastapi.security import OAuth2PasswordRequestForm
import database

models.Base.metadata.create_all(bind=database.engine)

app = fastapi.FastAPI()


@app.post("/api/users")
async def create_user(
    user: schemas.UserCreate, db: orm.Session = fastapi.Depends(crud.get_db)
):
    db_user = await crud.get_user_by_email(email=user.email, db=db)
    if db_user:
        raise fastapi.HTTPException(status_code=400, detail="Email already in use")
    
    
    user = await crud.create_user(user=user, db=db)

    return await crud.create_token(user=user)


@app.post("/api/token")
async def generate_token(
    form_data: OAuth2PasswordRequestForm = fastapi.Depends(),
    db: orm.Session = fastapi.Depends(crud.get_db),
):
    user = await crud.authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise fastapi.HTTPException(status_code=401, detail="Ivalid Credentials")

    return await crud.create_token(user)


@app.get("/api/users/me", response_model=schemas.User)
async def get_ser(user: schemas.User = fastapi.Depends(crud.get_current_user)):
    return user


@app.post("/api/leads", response_model=schemas.Lead)
async def create_lead(
    lead: schemas.LeadCreate,
    user: schemas.User = fastapi.Depends(crud.get_current_user),
    db: orm.Session = fastapi.Depends(crud.get_db),
):
    return await crud.create_lead(lead=lead, user=user, db=db)


@app.get("/api/leads", response_model=List[schemas.Lead])
async def get_lead(
    user: schemas.User = fastapi.Depends(crud.get_current_user),
    db: orm.Session = fastapi.Depends(crud.get_db),
):
    return await crud.get_leads(user=user, db=db)


@app.get("/api/leads/{id}", response_model=schemas.Lead)
async def get_lead(
    id: int,
    user: schemas.User = fastapi.Depends(crud.get_current_user),
    db: orm.Session = fastapi.Depends(crud.get_db),
):
    return await crud.get_lead(id=id, user=user,db=db)


@app.delete("/api/leads/{id}", status_code=204)
async def delete_lead(
    id: int,
    user: schemas.User = fastapi.Depends(crud.get_current_user),
    db: orm.Session = fastapi.Depends(crud.get_db),
):
    await crud.delete_lead(id=id, user=user,db=db)
    return {"message": "Succesfuly Deleted"}

@app.put("/api/leads/{id}", status_code=200)
async def update_lead(
    id: int,
    lead: schemas.LeadCreate,
    user: schemas.User = fastapi.Depends(crud.get_current_user),
    db: orm.Session = fastapi.Depends(crud.get_db),
):
    return await crud.update_lead(id=id, lead=lead, user=user, db=db)


@app.get("/api")
async def root():
    return {"message":"Awesome Leads"}