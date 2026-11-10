import logging

from sqlmodel import Session

from app import crud
from app.core.authorization import Role
from app.core.config import settings
from app.core.db import engine, init_db
from app.models import UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# One account per non-admin role, so every role can be tried locally.
# They share the first admin's password (FIRST_SUPERUSER_PASSWORD).
DEMO_USERS: dict[str, Role] = {
    "manager@example.com": Role.MANAGER,
    "member@example.com": Role.MEMBER,
}


def seed_demo_users(session: Session) -> None:
    for email, role in DEMO_USERS.items():
        if crud.get_user_by_email(session=session, email=email):
            continue
        crud.create_user(
            session=session,
            user_create=UserCreate(
                email=email,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                full_name=f"Demo {role.value.title()}",
                role=role,
            ),
        )
        logger.info("Created demo user %s with role %s", email, role.value)


def init() -> None:
    with Session(engine) as session:
        init_db(session)
        if settings.FASTAPI_ENV == "development":
            seed_demo_users(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
