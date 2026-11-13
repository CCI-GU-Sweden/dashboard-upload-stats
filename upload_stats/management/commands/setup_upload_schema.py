from dashboard.schema_setup import SchemaSetupCommand


class Command(SchemaSetupCommand):
    help = 'Check or explicitly create the PostgreSQL upload statistics baseline.'
    package = 'upload_stats'
    tables = ('imports',)
