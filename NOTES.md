# Notes

## What was done

- Backend RBAC with three roles, a permission map, a migration, a metrics
  endpoint, seeded users per role, and logging of denied attempts.
- Frontend: permission-aware navigation and buttons, "Access denied" page,
  role select in the user forms, metrics page.
- Backend tests for the permission matrix and for privilege-escalation attempts.
- README, two ADRs and a diagram.

## Scope cuts and known gaps

- **End-to-end coverage of roles is thin.** The template's Playwright suite
  was adapted to the role select and the "Access denied" page and passes
  locally (62 tests), but only the member-is-denied case is role-specific.
  The manager's read-only view was checked by hand. Playwright does not run
  in CI.
- **No "last admin" count check.** An admin cannot delete their own account
  (kept from the template) or change their own role, so an admin cannot lock
  themselves out. Two admins could still demote each other; a check that at
  least one admin remains would close that.
- **Tests share the development database** and delete all users at the end.
  This is template behaviour; a separate test database would be the fix.
- **`FIRST_SUPERUSER` names were kept** in `.env` and the settings. They are
  deployment configuration that existing environments already set. The user
  they create has the `admin` role. Test fixtures and test names were renamed
  to "admin" in a separate, mechanical commit.
- **The `/admin` URL was kept** for the users page (now titled "Users") to
  avoid breaking links; managers can open it read-only.
- **CI was trimmed to what applies here.** One workflow runs the backend lint,
  type checks and tests on every pull request. The template's other workflows
  (releases, deployments, issue and dependency bots, Playwright) were removed:
  they maintain the template itself or need secrets this repository does not
  have.

## Behaviour changes worth knowing

- An invalid or expired token now returns `401` instead of `403`, so clients
  can tell "log in again" from "not allowed".
- The `is_superuser` field is gone from the API; `role` and `permissions`
  replace it.

## With more time

- Extend the Playwright suite with one test per role and run it in CI.
- Runtime-editable roles (permissions in the database) if the product needs it.
- An audit trail for role changes, not just a log line for denials.
- Use a router-level guard so a forbidden page does not render the layout first.

## Tools

Built with AI assistance (Claude Code). The template was audited for hidden
install hooks and disguised files before anything was run.
