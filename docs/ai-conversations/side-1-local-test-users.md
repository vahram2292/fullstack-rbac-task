# AI conversation 2 (side): test users for local checking

Tool: Claude Code (desktop app), model Claude Fable 5.2. Date: 2026-11-10.

A side conversation forked from the main one (see task-1-rbac.md). Only the part after the fork is shown; everything before it is identical to the main conversation.

Converted from the app's session export to Markdown. For readability and
privacy:

- Each tool action (shell command, file edit, browser step) is shown as a
  one-line note instead of its raw input and output.
- System prompts, the assistant's internal reasoning and images are left out.
- Local paths, email addresses and session ids are replaced by placeholders.

---

**USER**

five me users so I can test all locally

> _Ran a command: Check the app is running and the three test users can log in_

**ASSISTANT**

The app is running at http://localhost:8000 and all three test users log in (I just checked each one):

| Role | Email | Password |
|---|---|---|
| admin | `admin@example.com` | `changethis` |
| manager | `manager@example.com` | `changethis` |
| member | `member@example.com` | `changethis` |

What to expect for each:

- **Admin:** sees Dashboard, Items, Metrics and Users; can add, edit and delete users and change their role.
- **Manager:** sees Metrics and a read-only Users list, with no Add User button and no row actions.
- **Member:** sees only Dashboard and Items; opening `/admin` or `/metrics` directly shows "Access denied" without logging you out.

Running the backend tests deletes all users. If the logins stop working afterwards, bring the users back with:

```bash
docker compose exec backend bash scripts/prestart.sh
```
