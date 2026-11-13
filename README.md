# dashboard-upload-stats

Upload statistics module for the [CCI Django dashboard](https://github.com/CCI-GU-Sweden/Dashboard-django). This is an early extraction: it provides the upload pages and API, but still depends on the dashboard core for authentication, permissions, base templates and shared frontend assets. It is not a standalone Django project.

The app reads an existing PostgreSQL `imports` table on the connection's search path and does not modify it. It expects the columns `scope`, `time`, `username`, `file_count`, `total_file_size_mb` and `import_time_s`. The database role needs `SELECT` access. The existing [Omero_GU uploader](https://github.com/CCI-GU-Sweden/Omero_GU) creates this table and records uploads; its scheduled rollup compacts records. The uploader is a separate application and is not included in this module. Other installations need a compatible producer or their own data import; a fresh standalone data collector is not yet provided.

## Development integration

Install this package in the same Python environment as a compatible core checkout, add `upload_stats` to `INSTALLED_APPS`, and include `upload_stats.urls` in the core URL configuration. The in-progress core has an upload enable switch; it must reference a compatible version of this package. Templates and JavaScript are included as package data.

Existing URLs are `/uploads/`, `/api/uploads/summary` and `/api/uploads/scopes`. Staff/admin access is checked by the core's `accounts.permissions.operational_access` helper. The package expects the core's shared Plotly and html2canvas assets.

The `upload_stats.dashboard_module.module` descriptor implements the core's version 1 module contract. Its overview supplies files, data volume and top microscope for the last 30 days. The core renders the card and requests its metrics separately; the module checks staff access and provides data without exposing usernames.

Run the frontend test from this repository with `node --test tests/uploads_frontend.test.js`. The dashboard core's Django tests also exercise the module's access checks and API integration.

With the module enabled, `python manage.py check_upload_schema` checks that the configured PostgreSQL connection can find and select the required columns without reading rows or changing schema/data. Use `--database ALIAS` for another configured Django database. The command does not validate column types, the uploader's write access, collector operation or full schema compatibility; it does not create or migrate the uploader-owned table. It can be used as an early preflight, not as a substitute for a versioned schema setup Job.

`python manage.py setup_upload_schema` performs a stricter baseline collision check. Add `--apply` to create `public.imports` only when no baseline objects exist. Matching tables are reused without changing data; partial or mismatching objects cause an error and rollback. This command uses the dashboard core's schema setup helper and requires a PostgreSQL setup identity able to create a temporary comparison schema and create objects in `public`. It does not grant runtime or uploader privileges. See `deploy/schema-setup-job.example.yaml` for an unconfigured Job; run setup once per release before starting dependent workloads. Confirm the uploader and dashboard use the same database and search path. Do not blindly replace the existing uploader's schema ownership.

## License

The repository is MIT licensed. Code extracted from Dashboard-django retains the copyright notice in [CORE_LICENSE](CORE_LICENSE).
