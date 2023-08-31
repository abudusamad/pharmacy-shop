import sqlalchemy.exc
from sqlalchemy import select

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from pharmacy_shop.database.models.admin import Admin
from pharmacy_shop.schema.admin import AdminCreate, AdminSchema
from pharmacy_shop.dependencies.database import DatabaseConnection, get_admin_or_404
from pharmacy_shop.security import Password

admins = APIRouter()


@admins.post("/admins", response_model=AdminSchema, tags=["admins"])
def create_user(admin_data: AdminCreate, database: DatabaseConnection) -> Admin:
    admin_data.password = Password.hash(admin_data.password)
    new_admin = Admin(**admin_data.model_dump())    

    try:
        database.add(new_admin)
        database.commit()
        database.refresh(new_admin)

        return new_admin
    except sqlalchemy.exc.IntegrityError:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="admin might already exist",
        )

    @admins.get("\current",response_model = [AdminSchema])
    def get_current_admin(admin: AuthenticatedUser) -> Admin:
        return Admin

@admins.get("/admins/", response_model=list[AdminSchema], tags=["admins"])
def get_all_users(database: DatabaseConnection) -> list[Admin]:
    try:
        db_admins: list[Admin | None] = database.scalars(select(Admin)).all()

        return db_admins
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No admins in the database.",
        )


@admins.get("/admins/{admin_id}", response_model=AdminSchema, tags=["admins"])
def get_user_by_id(admin_id: int, database: DatabaseConnection) -> Admin:
    db_admin: Admin | None = get_admin_or_404(admin_id=admin_id, database=database)
    return db_admin


@admins.delete("/admins/{admin_id}", response_model=dict[str, str], tags=["admins"])
def delete_admin_id(admin_id: int, database: DatabaseConnection):
    try:
        del_db_admin: Admin = get_admin_or_404(admin_id=admin_id, database=database)

        database.delete(del_db_admin)
        database.commit()
    except sqlalchemy.exc.InternalError:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Admin with id:{admin_id} could not be deleted!",
        )
    return {"msg": "Account successfully deleted!"}
