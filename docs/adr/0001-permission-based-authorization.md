# ADR 1: Permission-based checks with a central role map

## Problem

The template has one boolean, `is_superuser`, checked in a dependency and in
six inline `if` statements. We need three roles (admin, manager, member) and a
model a teammate can understand quickly and extend without touching many files.

## Options

1. **Role checks at each endpoint** (`require_role(ADMIN, MANAGER)`).
   Simple to read, but the meaning of a role is spread across every endpoint.
   Adding a role, or changing one, means revisiting all of them, and it is easy
   to miss one.
2. **Endpoints require a permission; one map says which role grants it.**
   Each endpoint states *what* it needs (`users:read`). The role-to-permission
   map is the only place roles are given meaning.
3. **A policy library or permissions stored in database tables** (Casbin,
   role/permission tables). Flexible and editable at runtime, but far more
   moving parts than three fixed roles justify.

## Decision

Option 2. `app/core/authorization.py` defines `Role`, `Permission` and
`ROLE_PERMISSIONS`. Endpoints use the `require_permission(...)` FastAPI
dependency; data-dependent rules call `has_permission(...)` in the endpoint.

The role is a text column on `user`, validated by the `Role` enum in the
application, and it is read from the database on each request rather than
embedded in the token.

## Trade-offs

- **Gained:** the whole model fits on one screen; adding a role is a one-file
  change; tests can assert the map directly; role changes apply immediately.
- **Accepted:** permissions are code, so changing them needs a deploy. If
  administrators ever need to edit roles at runtime, the map moves to a table
  and `permissions_for` becomes a query; endpoints would not change.
- **Accepted:** one role per user. Multiple roles would be a union of sets in
  `permissions_for`, again without touching endpoints.
- **Accepted:** a text column means the database does not reject an unknown
  role by itself. In exchange, adding a role needs no schema migration.
- **Accepted:** the per-request user lookup already existed in the template, so
  reading the role there costs nothing extra.
