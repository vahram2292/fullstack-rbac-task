"""The authorization model: roles, permissions, and which role grants what.

Endpoints ask for a *permission* (see `require_permission` in `app.api.deps`),
never for a role. Adding a role, or changing what a role may do, is an edit to
`ROLE_PERMISSIONS` and nothing else.
"""

from enum import StrEnum


class Role(StrEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"


class Permission(StrEnum):
    USERS_READ = "users:read"
    USERS_CREATE = "users:create"
    USERS_UPDATE = "users:update"
    USERS_DELETE = "users:delete"
    METRICS_READ = "metrics:read"
    ITEMS_MANAGE_ALL = "items:manage_all"
    SETTINGS_MANAGE = "settings:manage"


# Every logged-in user can read and update their own profile and their own
# items; that needs no permission. Permissions cover access beyond "own data".
ROLE_PERMISSIONS: dict[Role, frozenset[Permission]] = {
    Role.ADMIN: frozenset(Permission),
    Role.MANAGER: frozenset({Permission.USERS_READ, Permission.METRICS_READ}),
    Role.MEMBER: frozenset(),
}


def permissions_for(role: Role) -> frozenset[Permission]:
    return ROLE_PERMISSIONS[role]


def has_permission(role: Role, permission: Permission) -> bool:
    return permission in permissions_for(role)
