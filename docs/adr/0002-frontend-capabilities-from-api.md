# ADR 2: The frontend gets capabilities from the API

## Problem

The UI must hide links and buttons the user cannot use and show a friendly
message on pages they may not open. To do that it needs to know what the
current user is allowed to do.

## Options

1. **Check roles in the UI** (`user.role === "admin"`). The role-to-permission
   rules then exist twice, in Python and in TypeScript, and will drift apart.
2. **Send permissions from the API** with the current user, and have the UI ask
   `can("users:create")`.
3. **Put permissions in the token** and decode it in the browser. Avoids a
   request, but the list goes stale when a role changes, and the app already
   fetches the current user on load.

## Decision

Option 2. `UserPublic` has a computed `permissions` field, so `GET /users/me`
returns it with no extra endpoint. `usePermissions()` reads it from the existing
`currentUser` query. Navigation items declare a `requiredPermission`, and pages
are wrapped in `<RequirePermission>`, which renders an "Access denied" page
inside the normal layout.

`Role` and `Permission` types come from the generated API client, so a typo in
a permission name is a compile error.

## Trade-offs

- **Gained:** one source of truth. Changing what a role can do needs no
  frontend change at all.
- **Gained:** a `403` is now distinct from a `401`. Only `401` ends the session;
  previously any `403` logged the user out.
- **Accepted:** the UI check is a convenience, not security. Every rule is
  enforced again by the API, which the backend tests cover.
- **Accepted:** permissions are cached with the current user. A user whose role
  changes mid-session sees stale navigation until the next reload, but the API
  rejects anything they are no longer allowed to do. The cache is cleared on
  logout so permissions never carry over to the next account.
- **Accepted:** the guard is a component, not a router `beforeLoad` hook. It
  shares one code path with the sidebar and keeps the URL in place so the user
  sees why the page is unavailable, at the cost of rendering the layout first.
