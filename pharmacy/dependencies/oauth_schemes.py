from fastapi.security import OAuth2PasswordBearer

user_scheme = OAuth2PasswordBearer(tokenUrl="/users/authenticate", scheme_name="User")
admin_scheme = OAuth2PasswordBearer(
    tokenUrl="/admins/authenticate",
    scheme_name="Admin",
)
