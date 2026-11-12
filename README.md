# dashboard-upload-stats

Upload statistics module for the [CCI Django dashboard](https://github.com/CCI-GU-Sweden/Dashboard-django). This is an early extraction: it provides the upload pages and API, but still depends on the dashboard core for authentication, permissions, base templates and shared frontend assets. It is not a standalone Django project.

The app reads the existing PostgreSQL `public.imports` table and does not modify it. It expects the columns `scope`, `time`, `username`, `file_count`, `total_file_size_mb` and `import_time_s`. The database role needs `SELECT` access. The upload collector, schema creation and schema compatibility checks are not yet included; the legacy collector and its schema must be identified before a fresh installation is supported.

## Development integration

Install this package in the same Python environment as a compatible core checkout, add `upload_stats` to `INSTALLED_APPS`, and include `upload_stats.urls` in the core URL configuration. The in-progress core has an upload enable switch; it must reference a compatible version of this package. Templates and JavaScript are included as package data.

Existing URLs are `/uploads/`, `/api/uploads/summary` and `/api/uploads/scopes`. Staff/admin access is checked by the core's `accounts.permissions.operational_access` helper. The package expects the core's shared Plotly and html2canvas assets.

Run the frontend test from this repository with `node --test tests/uploads_frontend.test.js`. The dashboard core's Django tests also exercise the module's access checks and API integration.

## License

The repository is MIT licensed. Code extracted from Dashboard-django retains the copyright notice in [CORE_LICENSE](CORE_LICENSE).
