# AI conversation 3 (side): CI for the pull request

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

I see this line on the repo 🏭 CI (continuous integration) and CD (continuous deployment) based on GitHub Actions.

https://github.com/fastapi/full-stack-fastapi-template/tree/master is it okay that we skiped CI?

**ASSISTANT**

It's acceptable for the assignment, but it's the weakest spot in the submission and worth fixing.

**Why it's acceptable:** the assignment doesn't ask for CI. It grades code clarity, working RBAC, tests and setup docs, and `NOTES.md` states that the workflows were removed and why. Most of the 15 removed workflows are the template maintainers' own tooling (releases, deploys to their cloud, issue labelling, dependency bots) and would fail or do nothing in your repo.

**Why it's still a gap:**

- **A senior reviewer may read it as a shortcut.** "Removed CI" lands worse than "trimmed CI to what applies here". One of the removed workflows, `test-backend.yml`, just runs the backend tests and needs nothing beyond what the repo has, apart from an optional coverage-upload step. I removed it along with the rest, which was broader than necessary.
- **The PR shows no checks.** A green "81 tests passed" on the pull request is immediate proof the suite works, without the reviewer running anything.
- **`TEMPLATE_README.md` now over-claims.** It still carries the "CI and CD based on GitHub Actions" line and two status badges pointing at workflows that no longer exist.

**What I'd do:** add back one small workflow that runs the backend tests and lint on pull requests, and remove the dead badges and the CI/CD line from `TEMPLATE_README.md`. That is roughly 15 minutes, one extra commit on the PR, and `NOTES.md` would then say "CI trimmed to backend tests".

The main risk is that the first run fails on GitHub for an environment reason, which I'd fix before you send the link.

Do you want me to add it?

---

**USER**

yes please do that and inform main sesion

> _Ran a command: Read the template's original backend test workflow and the lines that mention CI_
> _Ran a command: Add the trimmed CI workflow, fix the docs that mention CI, commit and push to the pull request_
> _Used tool `get_status`_
> _Ran a command: Look at the workflow runs GitHub started for the new commit_
> _Ran a command: Wait for the first Test Backend run on the pull request to finish_

**ASSISTANT**

The new CI run passed on GitHub. I found the template's old workflows on `main` are still firing on the pull request, so I'm checking those before reporting.

> _Ran a command: List which workflows are active on the repo and what ran on the pull request_
> _Ran a command: Check for pull requests or branches opened on the repo by anyone other than us_
> _Used tool `SendMessage`_

**ASSISTANT**

CI is on the pull request and its first run passed on GitHub: lint, type checks, migration and seeding, the 81 tests, and the 90% coverage check. I've sent the details to the [main session](#<session-id>).

What changed (one new commit on [vahram2292/fullstack-rbac-task#1](https://github.com/vahram2292/fullstack-rbac-task/pull/1)):

- **Workflow:** `.github/workflows/test-backend.yml` is the template's backend test workflow, trimmed (no coverage upload) and with the lint step added. It runs on every pull request and on pushes to `main`.
- **`TEMPLATE_README.md`:** the two dead badges are gone, the line now says "CI" instead of "CI and CD", and a note at the top says it is the template's original README.
- **`NOTES.md` and `README.md`:** now say CI was trimmed to what applies here, not removed.

## A problem I found while checking the run

The untouched template baseline on `main` still contains the template's Dependabot config and all 15 of its workflows. Because `main` is the default branch, GitHub acts on them:

- **Dependabot opened three pull requests** on your public repo (#2, #3, #4), and it will keep opening more.
- **The template's old workflows run on those pull requests.** The Playwright one failed on #4, and one "Smokeshow" run failed.
- **Your pull request is green**, but it shows two extra checks from the old workflows ("main" and "Add to project") next to the real one.

A reviewer opening the repo would see four pull requests and some red marks that have nothing to do with your work. This comes from my choice to keep the baseline byte-identical to the template.

The fix I'd make:

1. Add one commit on `main` that removes the Dependabot config and the 14 workflows we don't keep.
2. Merge `main` into the feature branch, so the pull request stops showing those deletions.
3. Close the three Dependabot pull requests and delete their branches.

The catch is that `main` would no longer be a byte-identical copy of the template; it would be the template minus its GitHub automation, stated in the commit message. Leaving it as is means Dependabot keeps adding pull requests until you merge yours.
