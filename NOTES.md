# Notes

## What was done

- Backend RBAC with three roles, a permission map, a migration, a metrics
  endpoint, seeded users per role, and logging of denied attempts.
- Frontend: permission-aware navigation and buttons, "Access denied" page,
  role select in the user forms, metrics page.
- Backend tests for the permission matrix and for privilege-escalation attempts.
- README, two ADRs and a diagram.

## Scope cuts and known gaps

- **Playwright runs locally, not in CI.** The template's suite was adapted to
  the role select and the "Access denied" page, and `roles.spec.ts` adds one
  browser test per role (what a manager and a member can and cannot see).
  All pass locally; browser tests were kept out of CI to avoid a slow,
  flake-prone check.
- **"At least one admin" is guaranteed by rule, not by counting.** Only admins
  can change users, and an admin cannot demote, deactivate or delete
  themselves, so whoever makes a change is still an active admin afterwards.
  The one gap is two admins demoting each other in the same instant; closing
  that needs a row lock and was left out.
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

- Run the Playwright suite in CI.
- Runtime-editable roles (permissions in the database) if the product needs it.
- An audit trail for role changes, not just a log line for denials.
- Use a router-level guard so a forbidden page does not render the layout first.

## Tools

Built with AI assistance (Claude Code). The template was audited for hidden
install hooks and disguised files before anything was run.
The conversations are in
[docs/ai-conversations](./docs/ai-conversations/README.md).
