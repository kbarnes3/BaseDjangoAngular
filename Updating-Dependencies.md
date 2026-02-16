Updating Dependencies
=====================

Python Dependencies
-------------------

1. Make any needed updates to `requirements.in` and `dev-requirements.in`.
1. Run `Upgrade-Requirements` to update the pinned `requirements.txt` and `requirements-dev.txt`.
1. Run `uv pip sync requirements-dev.txt` to update your local environment.
1. If Django was updated, run `Invoke-Manage makemigrations` to create any needed migration files.
1. If any migrations were created, run `Invoke-Manage migrate` to apply them locally.
1. Test things out.
1. Commit the modified `requirements.txt` and `requirements-dev.txt` files.