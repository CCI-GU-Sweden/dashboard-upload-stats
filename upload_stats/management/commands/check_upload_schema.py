"""Check the existing uploader-owned table without changing data."""
from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError, connections


REQUIRED_COLUMNS = (
    'scope', 'time', 'username', 'file_count', 'total_file_size_mb', 'import_time_s',
)


class Command(BaseCommand):
    help = 'Check that the upload statistics table is present and readable.'

    def add_arguments(self, parser):
        parser.add_argument('--database', default='default', help='Django database alias (default: default).')

    def handle(self, *args, **options):
        database = connections[options['database']]
        if database.vendor != 'postgresql':
            raise CommandError('Upload statistics requires a PostgreSQL database.')
        try:
            with database.cursor() as cursor:
                if 'imports' not in database.introspection.table_names(cursor):
                    raise CommandError('Upload statistics table imports was not found on the database search path.')
                columns = {column.name for column in database.introspection.get_table_description(cursor, 'imports')}
                missing = sorted(set(REQUIRED_COLUMNS) - columns)
                if missing:
                    raise CommandError('Upload statistics table imports is missing columns: ' + ', '.join(missing))
                names = ', '.join(database.ops.quote_name(name) for name in REQUIRED_COLUMNS)
                cursor.execute(f'SELECT {names} FROM {database.ops.quote_name("imports")} WHERE 1 = 0')
        except DatabaseError as exc:
            raise CommandError('Could not inspect or read the upload statistics table; check the connection and SELECT permissions.') from exc
        self.stdout.write(self.style.SUCCESS('Upload statistics table exists and required columns are readable.'))
