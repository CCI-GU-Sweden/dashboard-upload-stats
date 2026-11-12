from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.core.management import call_command, CommandError
from django.db import DatabaseError
from django.test import SimpleTestCase

from upload_stats.management.commands.check_upload_schema import REQUIRED_COLUMNS


class UploadSchemaCheckTests(SimpleTestCase):
    def setUp(self):
        self.database = MagicMock()
        self.database.vendor = 'postgresql'
        self.cursor = self.database.cursor.return_value.__enter__.return_value
        self.database.introspection.table_names.return_value = ['imports']
        self.database.introspection.get_table_description.return_value = [SimpleNamespace(name=name) for name in REQUIRED_COLUMNS]
        self.database.ops.quote_name.side_effect = lambda value: '"' + value + '"'
        patcher = patch('upload_stats.management.commands.check_upload_schema.connections', {'default': self.database})
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_checks_required_columns_without_reading_rows(self):
        call_command('check_upload_schema')
        statement = self.cursor.execute.call_args.args[0]
        self.assertIn('WHERE 1 = 0', statement)
        self.assertIn('"imports"', statement)
        for name in REQUIRED_COLUMNS:
            self.assertIn('"' + name + '"', statement)

    def test_missing_table_or_columns_fails(self):
        self.database.introspection.table_names.return_value = []
        with self.assertRaisesMessage(CommandError, 'was not found'):
            call_command('check_upload_schema')
        self.database.introspection.table_names.return_value = ['imports']
        self.database.introspection.get_table_description.return_value = [SimpleNamespace(name='time')]
        with self.assertRaisesMessage(CommandError, 'missing columns'):
            call_command('check_upload_schema')
        self.cursor.execute.assert_not_called()

    def test_database_errors_and_other_engines_fail(self):
        self.cursor.execute.side_effect = DatabaseError('denied')
        with self.assertRaisesMessage(CommandError, 'SELECT permissions'):
            call_command('check_upload_schema')
        self.database.vendor = 'sqlite'
        with self.assertRaisesMessage(CommandError, 'requires a PostgreSQL'):
            call_command('check_upload_schema')
