# AI conversation 5: Task 2, one-click Ghost deploy on Hetzner behind a tunnel

Tool: Claude Code (desktop app), model Claude Fable 5.2. Date: 2026-11-10.

This conversation was forked from the main Task 1 conversation (see task-1-rbac.md). Only the part after the fork is shown. Its result is the repository https://github.com/vahram2292/ghost-hetzner-tunnel.

Converted from the app's session export to Markdown. For readability and
privacy:

- Each tool action (shell command, file edit, browser step) is shown as a
  one-line note instead of its raw input and output.
- System prompts, the assistant's internal reasoning and images are left out.
- Local paths, email addresses and session ids are replaced by placeholders.

---

**USER**

2 - infrastructure question task - Develop one click script to deploy ghost blog platform at a Hetzner VPS with no public SSH access, only through tunnels (any provider/app)

this is second task that they have aseked for

> _Used tool `start_session`_
> _Ran a command: Check where the interrupted RBAC commit and push ended up, and which infrastructure tools are installed_
> _Ran a command: Re-run the end-to-end suite on the current build and check the pull request's CI_
> _Ran a command: Wait for the RBAC pull request's CI run to finish_

**ASSISTANT**

## First, the RBAC task

The command that was cut off did complete. Both follow-up commits (the badge colour map and the test rename) are on the pull request, the backend CI passes, and I re-ran the end-to-end suite on the final build: 62 passed.

## The Ghost task as I read it

One command that takes an empty Hetzner account to a running Ghost blog, where the server accepts no SSH from the internet and admin access exists only through a tunnel.

The approach I'd take:

- **One script, `./deploy.sh`,** reading a small `.env` (Hetzner API token, tunnel token, domain). It calls the Hetzner API to create a firewall and a server, and passes a cloud-init file that does all the setup on first boot. Nobody ever SSHes in to install anything.
- **Firewall with zero inbound rules.** Port 22 is closed to the internet from the first second, not closed afterwards.
- **On the server:** Docker Compose with Ghost and MySQL 8 (Ghost requires MySQL in production), generated database passwords, automatic security updates, and the tunnel agent.
- **Extras:** a `destroy.sh`, a re-run-safe deploy, and a README with a diagram and the trade-offs.

## The tunnel choice

| | Cloudflare Tunnel | Tailscale |
|---|---|---|
| Blog reachable at | Your own domain, HTTPS by Cloudflare | A `…ts.net` address via Tailscale Funnel |
| SSH | Through Cloudflare Access | Tailscale SSH, only from your devices |
| Needs | A domain managed in Cloudflare | A free Tailscale account, no domain |
| Looks like production | Yes | More of a demo URL |

I recommend Cloudflare Tunnel if you have a domain you can put on Cloudflare, because the blog ends up on a real domain with no open ports at all. Without a domain, Tailscale is the only one of the two that works.

## Effort

About 1.5–2.5 hours including a real test deployment. The script itself is small; most of the time goes into testing a first boot end to end, since each attempt takes a few minutes. A test server costs a few cents (Hetzner bills hourly, about €4–5 a month for the smallest size).

## Other questions

1. **Hetzner account:** do you have one, and can you create an API token? I can't create accounts or handle your credentials, so you would put the tokens into the `.env` file yourself.
2. **Real test deploy:** are you fine with me creating (and afterwards deleting) a real server to prove it works? I'd confirm with you before anything billable is created.
3. **Should the blog itself also go only through the tunnel,** or is "no public SSH" enough and ports 80/443 may be open? I'd put everything through the tunnel; it is the stricter reading and simpler.
4. **Tooling:** did they hint at Bash, Terraform or Ansible? With no hint I'd use plain Bash plus cloud-init, since "one click script" suggests the fewest prerequisites.
5. **Delivery:** a second public repo under `vahram2292`, same Friday deadline?

---

**USER**

Cloudflare Tunnel

> _Started a helper agent: Verify Cloudflare and Hetzner APIs_
> _Ran a command: Create the project folder and check for local tools and an SSH public key_
> _Used tool `change_directory`_
> _Ran a command: Write the Ghost + MySQL + tunnel Compose file and boot Ghost and MySQL locally to prove the configuration works_

**ASSISTANT**

Ghost 6 with MySQL boots locally with the Compose file. Checking one error in its log and the HTTPS-behind-proxy behaviour before writing the deploy script.

> _Ran a command: Read the Ghost log error and test Ghost configured with an HTTPS address behind a simulated proxy_
> _Ran a command: Remove the local Ghost test containers and data_
> _Wrote file `cloud-init.yaml.tpl`_
> _Ran a command: Write the shared helper library, the example configuration file and gitignore_

**ASSISTANT**

The server setup file, Compose stack and shared helpers are written. I'm waiting for the API verification to come back before writing the deploy and destroy scripts, so the Cloudflare and Hetzner calls match the current documentation.

> _Ran a command: Add the HTTPS-header proxy to the stack, write the deploy and destroy scripts, and lint them_

**ASSISTANT**

Scripts are written and lint-clean. Now testing everything that can be tested without your tokens: the rendered server setup file, and the full container stack with the HTTPS proxy.

> _Ran a command: Render the server setup file with fake values and validate it with cloud-init's own schema checker_
> _Ran a command: Make the scripts sourceable for testing, then render and validate the server setup file again_
> _Ran a command: Fix the library path when the script is sourced, then render and validate the server setup file_

**ASSISTANT**

Server setup file validates against cloud-init's schema and renders correctly. Now booting the full stack locally with the HTTPS proxy in front of Ghost.

> _Ran a command: Boot Ghost, MySQL and the proxy locally with an HTTPS address and check the blog answers through the proxy_
> _Ran a command: Run the deploy script with no config, incomplete config and fake tokens to check it fails early with clear messages_
> _Wrote file `README.md`_

**ASSISTANT**

README is written. Committing locally (no push) with your GitHub noreply identity.

> _Ran a command: Initialise the repository with the project-only identity and commit the first version_

**ASSISTANT**

The second task is built and committed locally in `Documents/Projects/ghost-hetzner-tunnel`, but it has not been run against real accounts yet, and nothing is published.

## What it does

`./deploy.sh` reads four values from a `.env` file and then:

1. **Checks** both API tokens before creating anything.
2. **Cloudflare:** creates a tunnel, routes the blog hostname and an SSH hostname through it, creates the DNS records, and puts the SSH hostname behind a Cloudflare Access login for one email address.
3. **Hetzner:** creates a firewall with no inbound rules and a server with that firewall attached from the first second. Port 22 is never open to the internet.
4. **First boot:** the server sets itself up: Docker, SSH locked to loopback, Ghost 6 with MySQL 8, and the tunnel agent dialling out.
5. **Waits** for the blog to answer over HTTPS, then prints the URL and the SSH command.

`./destroy.sh` removes everything it created. The only local requirements are `bash`, `curl` and `jq`.

## What was tested

- The scripts pass `shellcheck` and run under macOS's built-in bash 3.2.
- The server setup file passes cloud-init's own schema check on Ubuntu 24.04.
- Ghost, MySQL and the proxy start locally with an HTTPS address and answer without redirect loops.
- The Cloudflare and Hetzner API calls were checked against the current documentation. That turned up three things my memory had wrong: Hetzner's `cx22` can no longer be ordered (now `cx23`), Cloudflare Access wants reusable policies, and DNS records need a `ttl`.
- With missing or fake config the script fails early with a clear message.

**Not tested:** a real deployment. The API calls, the tunnel connection, the SSH path through Access and the first boot on a real server have never run. The README says so in its last section. I would not submit an infrastructure script that has never deployed.

## One addition you didn't ask for

I added a small proxy container between the tunnel and Ghost. Ghost redirects forever unless it is told the visitor used HTTPS, and Cloudflare's docs don't confirm the tunnel forwards that header, so the proxy sets it explicitly.

## What a real test needs from you

- **Hetzner:** an API token with Read & Write for a project.
- **Cloudflare:** a domain already on your account, Zero Trust enabled once (free plan), and an API token with the four permissions listed in the README.
- **The `.env` file:** copy `.env.example` to `.env` and paste the tokens in yourself, not into this chat. The file is git-ignored.

The test creates one small server, costing a few cents if destroyed afterwards. I'll confirm with you before creating it and again before publishing the repo.

Files are in `Documents/Projects/ghost-hetzner-tunnel`:
- README.md
- deploy.sh
- destroy.sh
- server/cloud-init.yaml.tpl
- server/docker-compose.yml
- .env.example

---

**USER**

Submit untested

> _Ran a command: Add a status note to the README, then create the public GitHub repo and push_
> _Ran a command: Add the status note to the README and commit it locally_

**ASSISTANT**

The repo is ready to submit but is not on GitHub yet: the app's automatic safety check blocked the step that creates the public repo and pushes. I did not try to work around it.

What I did do:

- **Status note:** the README now says near the top that the script is statically verified and tested locally, but not yet run against live Hetzner and Cloudflare accounts. A reviewer sees that before anything else.
- **Committed locally:** two commits on `main`, using your GitHub noreply identity. No `.env`, keys or tokens are in the repo; it contains only the eight project files.

If you'd rather publish it yourself, this is the command I was going to run, from the project folder:

```bash
gh repo create vahram2292/ghost-hetzner-tunnel --public --source . --remote origin --push --description "One-command Ghost blog on a Hetzner VPS with no inbound ports: blog and SSH only through a Cloudflare Tunnel"
```

After it is up, the link to send them is `https://github.com/vahram2292/ghost-hetzner-tunnel`.

Because it is untested, expect the reviewers to run it. The parts most likely to fail on a first real run are the Cloudflare Access call and the first boot on the server. If you get Hetzner and Cloudflare tokens before Friday, a real test is worth doing even after you submit.

---

**USER**

Yes, publish it

> _Ran a command: Create the public GitHub repo and push the two commits_
> _Ran a command: Confirm the repo is public and contains only the expected files and commits_
> _Ran a command: List the published files and commits_

**ASSISTANT**

The second task is published: https://github.com/vahram2292/ghost-hetzner-tunnel

I confirmed the repo is public, on `main`, and contains only the eight project files and two commits, both under your GitHub noreply address. No `.env`, keys or tokens are in it.

It has still never been run against live Hetzner and Cloudflare accounts, and the README states that near the top. If you get tokens before Friday, tell me and I'll run a real deployment and fix whatever it turns up.

Both links for your submission:

- **Task 1 (RBAC):** https://github.com/vahram2292/fullstack-rbac-task/pull/1
- **Task 2 (Ghost deploy):** https://github.com/vahram2292/ghost-hetzner-tunnel

Open the Ghost README on GitHub once to check that the diagram renders, since I can't view it as GitHub displays it. The same applies to the RBAC README.

---

**USER**

pls double check all as I want to send it afterwords

> _Ran a command: Check the published state of the RBAC repo: branches, pull request, CI runs, commit identities, leaked secrets and broken links_
> _Ran a command: Inspect the two commits another session added, especially the published conversation transcript, for sensitive content_
> _Ran a command: Scan the published conversation transcript for private details_
> _Ran a command: Read the transcript lines that mention paths, interviews or the second task, and how the README refers to it_
> _Ran a command: Write a small local fake of the Hetzner and Cloudflare APIs for testing the scripts_
> _Ran a command: Run deploy twice and then destroy against the local fake APIs, under macOS's built-in bash_
> _Ran a command: Render the Ghost README's diagram with the Mermaid command-line tool to check its syntax_
> _Used tool `Read`_
> _Ran a command: Redraw the Ghost README diagram, correct the troubleshooting wording and the testing section, then re-render_
> _Used tool `Read`_
