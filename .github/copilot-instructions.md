# BaseDjangoAngular

A template repo combining a Django 6 (Python 3.12) backend (`back/`) with an Angular 21 frontend (`front/`). Intended to be copied into a new repo and personalized with `replacer.py` before becoming a real project.

## Layout

- `back/` — Django project. The project package is `newdjangosite/` and contains per-environment settings modules (`settings.py` for tests, `settings_dev.py`, `settings_daily.py`, `settings_staging.py`, `settings_prod.py`). Each env also has a matching `manage_<env>.py` and `wsgi_<env>.py`. `settings_base.py` holds shared config; per-env modules wildcard-import from it and override.
- `back/common/` and `back/users/` — Django apps. `users` defines a custom email-based `User` model (`AUTH_USER_MODEL = 'users.User'`) integrated with `django-allauth` in headless mode (`HEADLESS_ONLY = True`).
- `front/` — Angular CLI workspace (standard `ng` layout under `src/app/`).
- `scripts/` — PowerShell "Scripts To Rule Them All" entry points (`Bootstrap.ps1`, `Setup.ps1`, `Update.ps1`, `Console.ps1`, `Invoke-Manage.ps1`, `Invoke-Ng.ps1`, etc.). These are the canonical dev workflow on Windows.
- `fabric_utils/` + `fabfile.py` — Fabric tasks for server provisioning/deploy.
- `config/`, `server_scripts/` — Ubuntu 24.04 server config templates.
- `replacer.py`, `secret_key.py` — One-time setup helpers used when forking the template; not part of normal dev.

> ⚠️ **Do not run `replacer.py`** unless the user explicitly asks you to. It rewrites and renames files across the repo in place (personalizing the template with a new project name, domain, email, etc.) and is destructive / not idempotent. Treat any task touching this file as read-only by default.

## Build / test / lint

Python deps are managed with **uv** (`pyproject.toml` + `uv.lock`); Python is pinned to `>=3.12,<3.13`. Node is `^24.15.0 || >=26` and npm is pinned to v12 (CI uses Node 24).

Match what CI (`.github/workflows/test.yml`) runs:

```
uv sync
uv run pylint back
uv run pylint fabric_utils
uv run pylint fabfile.py
uv run pytest back
uv run fab -l

cd front
npm ci
npm run lint
npm run test-headless   # ng test --watch=false --reporters=junit --output-file=junit/TESTS.xml
npm run build           # production build
```

Single Django test: `uv run pytest back -k test_name` (or `back/<app>/tests.py::TestClass::test_method`). `pytest.ini` lives in `back/` and sets `DJANGO_SETTINGS_MODULE=newdjangosite.settings`, so always invoke pytest with `back` as a path argument from the repo root (not from inside `back/`) — the wrapper scripts and CI both do this.

Single Angular test: `cd front && npx ng test --include=src/app/path/to/file.spec.ts`.

To upgrade pinned deps: edit `pyproject.toml`, then `uv lock --upgrade && uv sync` (the `Upgrade-Requirements` PowerShell function does this). If Django changed, follow `Updating-Dependencies.md` and run `makemigrations`/`migrate`.

## Local dev workflow (Windows / PowerShell)

The expected entry point is `scripts\Console.ps1`, which sets up / refreshes the `.venv`, runs migrations, and exposes helper functions in the shell:

- `Invoke-Manage <args>` — runs `back/manage.py` in the venv with cwd set to `back/`. **Always use this (or run from `back/`) rather than invoking `manage.py` from the repo root** — Django apps are imported as top-level names (`common`, `users`, `newdjangosite`), not as `back.users`.
- `Invoke-Ng <args>` / `Invoke-Npm <args>` — run from `front/`.
- `Invoke-Fabric <args>` — runs Fabric tasks.
- `Start-Server` — launches `ng serve` and `manage.py runserver` together. The Angular dev server proxies API calls per `front/proxy.conf.json`.
- `Update-DevEnvironment` — re-runs `scripts\Update.ps1`.

`scripts\Setup.ps1 -GitClean` wipes untracked files including the local sqlite db.

## Conventions

- **Settings split:** never put runtime config directly in `settings_base.py` that should differ per environment — add it to the relevant `settings_<env>.py`. `settings.py` is the test-only entry point used by pytest.
- **Pylint config (`pylintrc`)** pushes `back/` onto `sys.path` via `init-hook` and loads `pylint_django` with `django-settings-module=back.newdjangosite.settings`. Max line length is 100; `missing-*-docstring` and `duplicate-code` are disabled. Match snake_case for funcs/vars, PascalCase for classes.
- **Auth:** `users.User` uses `email` as `USERNAME_FIELD` with no username field. Signup/login flows go through allauth headless endpoints under `/_allauth/`; custom adapter is `users.adapter.UserAdapter` and signup form is `users.forms.SignupForm`. The `ACCOUNT_CREATION_MODE` setting (`default` / `notify` / `disabled`) gates new account creation.
- **Git revision exposure:** the backend uses `dealer` (middleware + context processor) and the frontend generates `front/git-version.json` via `git-version.js` as part of `npm start` / `npm build`. Don't hand-edit `git-version.json`.
- **Deployment scope:** `Fabric-Deploy <Config>` (Fabric task `deploy`) is the standard deploy and is sufficient for almost everything in the repo — it pulls source, updates backend deps, builds the frontend, runs migrations, reloads uwsgi, and copies the per-env nginx file (`config/ubuntu-24.04/nginx/<config>.yourdomain.tld`) into `/etc/nginx/sites-enabled/` and reloads nginx. `Fabric-DeployGlobalConfig <Config>` (task `deploy_global_config`) is **only** for host-wide config: `/etc/nginx/nginx.conf` and global scripts under `config/ubuntu-24.04/global/`. Editing a per-env nginx template does **not** require `Fabric-DeployGlobalConfig`.
- **CI uses pinned action SHAs** (see `test.yml`); preserve that pattern when adding workflow steps. Renovate (`renovate.json`) manages updates.
