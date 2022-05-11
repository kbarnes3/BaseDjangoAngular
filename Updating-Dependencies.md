Updating Dependencies
=====================

Python Dependencies
-------------------

1. Make any needed updates to `requirements.in` and `dev-requirements.in`.
1. Run `Upgrade-Requirements` to update the pinned requirements.txt for Windows
1. Run `pip-sync win64-py310-dev-requirements.txt` to update your local environment
1. If Django was updated, run `Invoke-Manage makemigrations` to create any needed migration files
1. If any migrations were created, run `Invoke-Manage migrate` to apply them locally
1. Test things out
1. Run `Fabric-CompileRequirements -Upgrade` to update the pinned requirements.txt files for Ubuntu.
The `-Hosts` parameter can be a connection string to any server setup by following `Setup-Server-Environment.md`.
1. Commit the modified `ubuntu64-py310*requirements.txt` files.