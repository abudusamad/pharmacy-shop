import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from pharmacy.database.models.admins import Admin
from pharmacy.dependencies.auth import AuthenticatedAdmin, get_authenticated_admin
from pharmacy.dependencies.database import AnnotatedAdmin, Database
from pharmacy.dependencies.jwt import create_token
from pharmacy.schemas.admins import AdminCreate, AdminSchema
from pharmacy.schemas.tokens import Token
from pharmacy.security import get_hash, password_matches_hashed

router = APIRouter(prefix="/admins", tags=["Admins"])


@router.post("/", response_model=AdminSchema)
def create_admin(admin_data: AdminCreate, db: Database) -> Admin:
    admin_data.password = get_hash(admin_data.password)

    admin = Admin(**admin_data.model_dump())

    try:
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return admin
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="admin already exists",
        )


@router.get(
    "/",
    response_model=list[AdminSchema],
    dependencies=[Depends(get_authenticated_admin)],
)
def get_list_of_admins(db: Database) -> list[Admin]:
    return db.scalars(select(Admin)).all()


@router.post("/authenticate", response_model=Token)
def login_admin_for_access_token(
    db: Database, credentials: OAuth2PasswordRequestForm = Depends()
) -> dict[str, str]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="incorrect username or password",
    )
    admin: Admin | None = db.scalar(
        select(Admin).where(Admin.username == credentials.username)
    )

    if admin is None:
        raise credentials_exception

    if not password_matches_hashed(plain=credentials.password, hashed=admin.password):
        raise credentials_exception

    data = {"sub": str(admin.id)}
    token = create_token(data=data)

    return {"access_token": token, "token_type": "bearer"}


@router.get("/current", response_model=AdminSchema)
def get_current_admin(admin: AuthenticatedAdmin) -> Admin:
    return admin


@router.get(
    "/{admin_id}",
    response_model=AdminSchema,
    dependencies=[Depends(get_authenticated_admin)],
)
def get_admin(admin: AnnotatedAdmin) -> Admin:
    return admin


@router.delete(
    "/{admin_id}",
    dependencies=[Depends(get_authenticated_admin)],
)
def delete_admin(admin: AnnotatedAdmin, db: Database) -> None:
    db.delete(admin)
    db.commit()
