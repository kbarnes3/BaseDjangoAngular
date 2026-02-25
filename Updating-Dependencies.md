Updating Dependencies
=====================

Python Dependencies
-------------------

1. Make any needed updates to `pyproject.toml`.
1. Run `Upgrade-Requirements` to update the pinned `uv.lock` and sync your local environment.
1. If Django was updated, run `Invoke-Manage makemigrations` to create any needed migration files.
1. If any migrations were created, run `Invoke-Manage migrate` to apply them locally.
1. Test things out.
1. Commit the modified `uv.lock` file.