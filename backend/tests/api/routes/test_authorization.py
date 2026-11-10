"""Authorization tests: who is allowed to do what, and that roles cannot be escalated."""

import logging
from collections.abc import Callable

import pytest
from fastapi.testclient import TestClient
from httpx import Response
from sqlmodel import Session

from app.core.authorization import ROLE_PERMISSIONS, Role
from app.core.config import settings
from tests.utils.user import create_random_user, token_headers_for_new_user
from tests.utils.utils import random_email, random_lower_string

API = settings.API_V1_STR
Headers = dict[str, str]


@pytest.fixture(scope="module")
def headers_by_role(client: TestClient, db: Session) -> dict[Role, Headers]:
    return {
        role: token_headers_for_new_user(client=client, db=db, role=role)
        for role in Role
    }


def list_users(client: TestClient, headers: Headers) -> Response:
    return client.get(f"{API}/users/", headers=headers)


def create_user(client: TestClient, headers: Headers) -> Response:
    new_user = {"email": random_email(), "password": random_lower_string()}
    return client.post(f"{API}/users/", headers=headers, json=new_user)


def view_metrics(client: TestClient, headers: Headers) -> Response:
    return client.get(f"{API}/metrics/", headers=headers)


def view_own_profile(client: TestClient, headers: Headers) -> Response:
    return client.get(f"{API}/users/me", headers=headers)


def update_own_profile(client: TestClient, headers: Headers) -> Response:
    return client.patch(
        f"{API}/users/me", headers=headers, json={"full_name": "New Name"}
    )


OK, FORBIDDEN = 200, 403

# The permission matrix from the README, as executable expectations.
PERMISSION_MATRIX = [
    # action,            admin, manager,   member
    (list_users,         OK,    OK,        FORBIDDEN),
    (create_user,        OK,    FORBIDDEN, FORBIDDEN),
    (view_metrics,       OK,    OK,        FORBIDDEN),
    (view_own_profile,   OK,    OK,        OK),
    (update_own_profile, OK,    OK,        OK),
]  # fmt: skip

MATRIX_CASES = [
    pytest.param(action, role, expected_status, id=f"{action.__name__}-as-{role.value}")
    for action, *expected_statuses in PERMISSION_MATRIX
    for role, expected_status in zip(
        (Role.ADMIN, Role.MANAGER, Role.MEMBER), expected_statuses, strict=True
    )
]


@pytest.mark.parametrize(("action", "role", "expected_status"), MATRIX_CASES)
def test_permission_matrix(
    client: TestClient,
    headers_by_role: dict[Role, Headers],
    action: Callable[[TestClient, Headers], Response],
    role: Role,
    expected_status: int,
) -> None:
    response = action(client, headers_by_role[role])

    assert response.status_code == expected_status


def test_every_role_has_a_permission_mapping() -> None:
    assert set(ROLE_PERMISSIONS) == set(Role)


@pytest.mark.parametrize("headers", [{}, {"Authorization": "Bearer not-a-valid-token"}])
def test_request_without_valid_token_is_unauthorized(
    client: TestClient, headers: Headers
) -> None:
    response = list_users(client, headers)

    assert response.status_code == 401


def test_member_cannot_escalate_own_role_through_profile_update(
    client: TestClient, headers_by_role: dict[Role, Headers]
) -> None:
    member_headers = headers_by_role[Role.MEMBER]

    response = client.patch(
        f"{API}/users/me", headers=member_headers, json={"role": "admin"}
    )

    assert response.json()["role"] == "member"
    assert list_users(client, member_headers).status_code == 403


def test_signup_always_creates_a_member(client: TestClient) -> None:
    signup_data = {
        "email": random_email(),
        "password": random_lower_string(),
        "role": "admin",
    }

    response = client.post(f"{API}/users/signup", json=signup_data)

    assert response.status_code == 200
    assert response.json()["role"] == "member"
    assert response.json()["permissions"] == []


def test_manager_cannot_change_or_delete_other_users(
    client: TestClient, headers_by_role: dict[Role, Headers], db: Session
) -> None:
    manager_headers = headers_by_role[Role.MANAGER]
    other_user_url = f"{API}/users/{create_random_user(db).id}"

    promote = client.patch(
        other_user_url, headers=manager_headers, json={"role": "admin"}
    )
    delete = client.delete(other_user_url, headers=manager_headers)

    assert promote.status_code == 403
    assert delete.status_code == 403


def test_role_change_by_admin_takes_effect_immediately(
    client: TestClient, headers_by_role: dict[Role, Headers], db: Session
) -> None:
    member_headers = token_headers_for_new_user(client=client, db=db, role=Role.MEMBER)
    member_id = view_own_profile(client, member_headers).json()["id"]
    assert view_metrics(client, member_headers).status_code == 403

    promote = client.patch(
        f"{API}/users/{member_id}",
        headers=headers_by_role[Role.ADMIN],
        json={"role": "manager"},
    )

    assert promote.status_code == 200
    assert view_metrics(client, member_headers).status_code == 200


def test_admin_cannot_change_own_role(
    client: TestClient, headers_by_role: dict[Role, Headers]
) -> None:
    admin_headers = headers_by_role[Role.ADMIN]
    admin_id = view_own_profile(client, admin_headers).json()["id"]

    response = client.patch(
        f"{API}/users/{admin_id}", headers=admin_headers, json={"role": "member"}
    )

    assert response.status_code == 403
    assert view_own_profile(client, admin_headers).json()["role"] == "admin"


def test_role_cannot_be_cleared(
    client: TestClient, headers_by_role: dict[Role, Headers], db: Session
) -> None:
    response = client.patch(
        f"{API}/users/{create_random_user(db).id}",
        headers=headers_by_role[Role.ADMIN],
        json={"role": None},
    )

    assert response.status_code == 422


def test_denied_attempt_is_logged(
    client: TestClient,
    headers_by_role: dict[Role, Headers],
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.WARNING, logger="app.api.deps"):
        view_metrics(client, headers_by_role[Role.MEMBER])

    assert "Authorization denied" in caplog.text
    assert "permission=metrics:read" in caplog.text
