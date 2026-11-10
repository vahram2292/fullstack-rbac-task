from fastapi import APIRouter, Depends
from sqlmodel import col, func, select

from app.api.deps import SessionDep, require_permission
from app.core.authorization import Permission, Role
from app.models import Item, MetricsPublic, User

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get(
    "/",
    dependencies=[Depends(require_permission(Permission.METRICS_READ))],
    response_model=MetricsPublic,
)
def read_metrics(session: SessionDep) -> MetricsPublic:
    """
    Usage metrics for the whole application.
    """
    user_counts_by_role = dict(
        session.exec(select(User.role, func.count()).group_by(col(User.role))).all()
    )
    active_users = session.exec(
        select(func.count()).select_from(User).where(col(User.is_active))
    ).one()
    total_items = session.exec(select(func.count()).select_from(Item)).one()

    return MetricsPublic(
        total_users=sum(user_counts_by_role.values()),
        active_users=active_users,
        users_by_role={role: user_counts_by_role.get(role, 0) for role in Role},
        total_items=total_items,
    )
