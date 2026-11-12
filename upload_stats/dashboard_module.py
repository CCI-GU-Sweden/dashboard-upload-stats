"""Dashboard core module contract, version 1."""
from accounts.permissions import operational_access
from dashboard.modules import DashboardModule

from . import data


def overview_metrics(user):
    summary = data.upload_summary({'period': '30'})
    top_scope = summary['top_scope_files']
    return [
        {'label': 'Files imported', 'value': f"{summary['total_files']:,}"},
        {'label': 'Total data', 'value': f"{summary['total_size_gb']:,.2f} GB"},
        {'label': 'Top microscope', 'value': top_scope['name'] if top_scope else '—'},
    ]


module = DashboardModule(
    key='uploads',
    name='Uploads',
    eyebrow='Data ingestion',
    icon='↑',
    url_name='uploads',
    urlconf='upload_stats.urls',
    can_view=operational_access,
    get_metrics=overview_metrics,
)
