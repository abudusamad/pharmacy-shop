from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"])


def get_hash(password: str) -> str:
    return password_context.hash(secret=password)


def password_matches_hashed(plain: str, hashed: str) -> bool:
    return password_context.verify(secret=plain, hash=hashed)
