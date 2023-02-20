import models
import sqlalchemy.orm as orm
import schemas
import passlib.hash as hash
import jwt
import fastapi
from fastapi.security import OAuth2PasswordBearer
import database
import datetime as dt

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


oathschema = OAuth2PasswordBearer(tokenUrl="/api/token")
ALGORITHM = "HS256"
JWT_SECRET = "myjwtsecret"


async def get_user_by_email(email: str, db: orm.Session):
    return db.query(models.User).filter(models.User.email == email).first()


async def create_user(user: schemas.UserCreate, db: orm.Session):
    user_obj = models.User(
        email=user.email, hashed_password=hash.bcrypt.hash(user.hashed_password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def authenticate_user(email: str, password: str, db: orm.Session):
    user = await get_user_by_email(email=email, db=db)
    if not user:
        return False

    if not user.verify_password(password=password):
        return False

    return user


async def create_token(user: models.User):
    user_obj = schemas.User.from_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    return dict(access_token=token, token_type="bearer")


async def get_current_user(
    db: orm.Session = fastapi.Depends(get_db), token: str = fastapi.Depends(oathschema)
):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(status_code=401, detail="Invalid email or password")

    return schemas.User.from_orm(user)


async def create_lead(lead: schemas.LeadCreate, user: schemas.User, db: orm.Session):
    lead_obj = models.Lead(**lead.dict(), owner_id=user.id)
    db.add(lead_obj)
    db.commit()
    db.refresh(lead_obj)
    return schemas.Lead.from_orm(lead_obj)


async def get_leads(user: schemas.User, db: orm.Session):
    leads = db.query(models.Lead).filter_by(owner_id=user.id)
    return list(map(schemas.Lead.from_orm, leads))


async def lead_selector(id: int, user: schemas.User, db: orm.Session):
    lead_obj = (
        db.query(models.Lead)
        .filter_by(owner_id=user.id)
        .filter(models.Lead.id == id)
        .first()
    )
    if lead_obj is None:
        raise fastapi.HTTPException(status_code=404, detail="Lead does not exist")

    return lead_obj


async def get_lead(id: int, user: schemas.User, db: orm.Session):
    lead = await lead_selector(id=id, user=user, db=db)

    return lead


async def delete_lead(id: int, user: schemas.User, db: orm.Session):

    lead = await lead_selector(id=id, user=user, db=db)
    db.delete(lead)
    db.commit()
    return lead

async def update_lead(id: int, lead: schemas.LeadCreate, user: schemas.User, db: orm.Session):
    lead_db = await lead_selector(id=id, user=user, db=db)
    lead_db.first_name = lead.first_name
    lead_db.last_name = lead.last_name
    lead_db.last_name = lead.last_name
    lead_db.last_name = lead.last_name
    lead_db.last_name = lead.last_name
    lead_db.date_last_updated = dt.datetime.utcnow()


    db.commit()
    db.refresh(lead_db)


    return schemas.Lead.from_orm(lead_db)