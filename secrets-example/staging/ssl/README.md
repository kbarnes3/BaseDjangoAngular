SSL certificate for the staging deployment
==========================================

`fab deploy staging` copies every file matching `staging.yourdomain.tld.*` from this
directory into `/etc/nginx/ssl` on the server, then chowns them to root with mode 644.

`config/$os$/nginx/staging.yourdomain.tld` expects exactly two files here:

- `staging.yourdomain.tld.crt` - the full certificate chain
- `staging.yourdomain.tld.key` - the matching private key

Both are required. All four deployment configs terminate TLS, so a certificate must be
present here before the config can be deployed. If you do not want to deploy SSL files for
a config, set `ssl` to `False` for it in the `CONFIGURATIONS` dict in
`fabric_utils/deploy.py` and serve that config over plain HTTP instead.

These files are intentionally absent from this example directory; never commit a real
private key to a public repo.