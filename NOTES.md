# Notes

## What was done

- Backend RBAC with three roles, a permission map, a migration, a metrics
  endpoint, seeded users per role, and logging of denied attempts.
- Frontend: permission-aware navigation and buttons, "Access denied" page,
  role select in the user forms, metrics page.
- Backend tests for the permission matrix and for privilege-escalation attempts.
- README, two ADRs and a diagram.

## Scope cuts and known gaps

- **Playwright tests were updated but not run.** The specs that referred to the
  old "Is superuser?" checkbox were adapted to the role select and the
  "Access denied" page. The UI was checked by hand in a browser as each of the
  three roles instead.
- **No "last admin" protection.** An admin cannot delete their own account
  (kept from the template), but an admin can still demote themselves or the only
  other admin. I would add a guard in `update_user`.
- **Tests share the development database** and delete all users at the end.
  This is template behaviour; a separate test database would be the fix.
- **`FIRST_SUPERUSER` names were kept** in `.env`, the settings and the test
  fixtures. They are deployment configuration and renaming them would have
  touched many unrelated files. The user they create has the `admin` role.
- **The `/admin` URL was kept** for the users page (now titled "Users") to
  avoid breaking links; managers can open it read-only.
- **Upstream GitHub workflows were removed.** They deploy and release the
  template itself and need secrets this repository does not have.

## Behaviour changes worth knowing

- An invalid or expired token now returns `401` instead of `403`, so clients
  can tell "log in again" from "not allowed".
- The `is_superuser` field is gone from the API; `role` and `permissions`
  replace it.

## With more time

- Run and extend the Playwright suite with one test per role.
- Runtime-editable roles (permissions in the database) if the product needs it.
- An audit trail for role changes, not just a log line for denials.
- Use a router-level guard so a forbidden page does not render the layout first.

## Tools

Built with AI assistance (Claude Code). The template was audited for hidden
install hooks and disguised files before anything was run.
