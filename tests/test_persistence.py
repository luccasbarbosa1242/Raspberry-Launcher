"""Persistence checks use temporary homes, including pre-phase-1 databases."""

import json
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from backend.database.migrations import initialize_database, run_sql_safely
from backend.emulators.emulator_manager import EmulatorManager
from backend.emulators.emulator_repository import EmulatorRepository
from backend.emulators.package_resolver import PackageResolver
from backend.database.database import database_scope
from backend.path_resolver import PathResolver


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.home = Path(temporary.name)
        self.environment = patch.dict(os.environ, RASPBERRY_LAUNCHER_HOME=str(self.home))
        self.environment.start()
        self.addCleanup(self.environment.stop)
        (self.home / "DATA").mkdir()

    def connect(self):
        connection = sqlite3.connect(self.home / "DATA" / "library.db")
        connection.row_factory = sqlite3.Row
        self.addCleanup(connection.close)
        return connection

    def legacy_database(self):
        connection = self.connect()
        folder = PathResolver.project_root() / "backend" / "database"
        run_sql_safely(connection, (folder / "schema.sql").read_text())
        for path in sorted((folder / "migrations").glob("00[1-8]_*.sql")):
            run_sql_safely(connection, path.read_text())
        connection.execute(
            """INSERT INTO games(id,title,type,platform,path,launch_type,installed,
                favorite,play_time,last_played) VALUES(?,?,?,?,?,?,?,?,?,?)""",
            ("kept", "Preservado", "native", "linux", "/existing/game", "linux", 1, 1, 123,
             "2026-10-20 12:00:00"),
        )
        connection.execute(
            """INSERT INTO game_versions(id,game_id,platform,path,launch_type,installed)
            VALUES('kept_linux','kept','linux','/existing/game','linux',1)"""
        )
        connection.execute(
            """INSERT INTO emulators(id,name,version,install_path,executable_path,installed,plugin_id)
            VALUES('pcsx2','Meu PCSX2','custom','/existing/emulator','/existing/emulator/run',1,'pcsx2')"""
        )
        connection.execute(
            """INSERT INTO emulator_packages(id,name,version,download_url,executable)
            VALUES('old-package','Pacote legado','0.1','https://example.invalid/old.zip','old.exe')"""
        )
        connection.commit()
        return connection

    def test_new_database_has_catalog_installations_and_future_identity_models(self):
        initialize_database()
        connection = self.connect()
        tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertTrue({
            "games", "game_versions", "platforms", "emulators", "emulator_packages",
            "game_installations", "game_version_installations", "emulator_installations",
            "profiles", "profile_game_state", "catalog_sources", "external_game_ids",
        } <= tables)
        self.assertEqual(connection.execute("SELECT count(*) FROM profiles").fetchone()[0], 0)
        self.assertEqual(connection.execute("SELECT count(*) FROM external_game_ids").fetchone()[0], 0)
        packages = connection.execute("SELECT * FROM emulator_packages WHERE emulator_id='pcsx2'").fetchall()
        self.assertEqual({row['system'] for row in packages}, {"linux", "windows"})
        self.assertEqual({row['architecture'] for row in packages}, {"x86_64"})
        platform = connection.execute("SELECT * FROM platforms WHERE id='ps2'").fetchone()
        self.assertTrue(json.loads(platform['examples_json']))
        self.assertEqual(platform['emulator_id'], 'pcsx2')

    def test_migration_preserves_legacy_ids_personal_data_packages_and_installations(self):
        self.legacy_database()
        initialize_database()
        connection = self.connect()
        game = connection.execute("SELECT * FROM games WHERE id='kept'").fetchone()
        self.assertEqual((game['favorite'], game['play_time'], game['last_played']),
                         (1, 123, '2026-10-20 12:00:00'))
        version = connection.execute("SELECT * FROM game_versions WHERE id='kept_linux'").fetchone()
        self.assertEqual((version['game_id'], version['path'], version['installed']),
                         ('kept', '/existing/game', 1))
        emulator = connection.execute("SELECT * FROM emulator_installations WHERE emulator_id='pcsx2'").fetchone()
        self.assertEqual((emulator['version'], emulator['executable_path'], emulator['installed']),
                         ('custom', '/existing/emulator/run', 1))
        self.assertEqual(connection.execute("SELECT name FROM emulators WHERE id='pcsx2'").fetchone()[0], 'Meu PCSX2')
        old = connection.execute("SELECT * FROM emulator_packages WHERE id='old-package'").fetchone()
        self.assertEqual((old['id'], old['version'], old['download_url']),
                         ('old-package', '0.1', 'https://example.invalid/old.zip'))

    def test_repeated_initialization_preserves_edits_and_never_rereads_seed_json(self):
        initialize_database()
        connection = self.connect()
        connection.execute("UPDATE platforms SET name='Plataforma editada',examples_json='[]' WHERE id='ps2'")
        connection.execute("UPDATE emulator_packages SET download_url='https://example.invalid/edited.zip' WHERE system='linux'")
        connection.commit()
        count = connection.execute("SELECT count(*) FROM emulator_packages").fetchone()[0]
        migrations = connection.execute("SELECT count(*) FROM migrations").fetchone()[0]
        (self.home / "DATA" / "emulator_packages.json").write_text('not valid JSON')
        initialize_database()
        initialize_database()
        self.assertEqual(connection.execute("SELECT count(*) FROM emulator_packages").fetchone()[0], count)
        self.assertEqual(connection.execute("SELECT count(*) FROM migrations").fetchone()[0], migrations)
        self.assertEqual(connection.execute("SELECT name FROM platforms WHERE id='ps2'").fetchone()[0], 'Plataforma editada')
        with patch('backend.emulators.package_resolver.PlatformDetector.current', return_value='linux'), \
             patch('backend.emulators.package_resolver.platform.machine', return_value='x86_64'):
            package = PackageResolver().get('pcsx2')
        self.assertEqual(package['download_url'], 'https://example.invalid/edited.zip')

    def test_custom_runtime_seed_imports_once_and_resolver_reads_database(self):
        seed = {'custom': {'name': 'Custom', 'plugin_id': None, 'packages': {'linux': {
            'version': '1', 'download_url': 'https://example.invalid/custom.zip',
            'archive_type': 'zip', 'executable': 'runner', 'architecture': 'aarch64',
        }}}}
        seed_file = self.home / 'DATA' / 'emulator_packages.json'
        seed_file.write_text(json.dumps(seed))
        initialize_database()
        seed_file.write_text('{}')
        with patch('backend.emulators.package_resolver.PlatformDetector.current', return_value='linux'), \
             patch('backend.emulators.package_resolver.platform.machine', return_value='arm64'):
            package = PackageResolver().get('custom')
        self.assertEqual((package['emulator_id'], package['architecture']), ('custom', 'aarch64'))
        self.assertEqual(package['download_url'], 'https://example.invalid/custom.zip')

    def test_x64_packages_are_not_selected_on_arm(self):
        initialize_database()
        with patch('backend.emulators.package_resolver.PlatformDetector.current', return_value='linux'), \
             patch('backend.emulators.package_resolver.platform.machine', return_value='aarch64'):
            with self.assertRaisesRegex(RuntimeError, 'linux/aarch64'):
                PackageResolver().get('pcsx2')

    def test_incompatible_installed_package_is_not_reused(self):
        initialize_database()
        binary = self.home / 'emulator'
        binary.write_bytes(b'fixture')
        connection = self.connect()
        package_id = connection.execute("SELECT id FROM emulator_packages WHERE system='linux'").fetchone()[0]
        with database_scope():
            EmulatorRepository().save(dict(id='pcsx2',name='PCSX2',plugin_id='pcsx2',package_id=package_id,
                version='2.7.424',install_path=str(binary.parent),executable_path=str(binary),installed=1))
            with patch('backend.emulators.emulator_manager.PlatformDetector.current', return_value='linux'), \
                 patch('backend.emulators.emulator_manager.current_architecture', return_value='aarch64'):
                self.assertFalse(EmulatorManager().is_installed('pcsx2'))

    def test_failed_seed_import_rolls_back_entire_migration_and_can_be_retried(self):
        (self.home / 'DATA' / 'emulator_packages.json').write_text('invalid JSON')
        with self.assertRaisesRegex(ValueError, 'cadastro inicial'):
            initialize_database()
        connection = self.connect()
        self.assertEqual(connection.execute("SELECT count(*) FROM migrations WHERE id LIKE '009_%'").fetchone()[0], 0)
        tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertNotIn('emulator_installations', tables)
        (self.home / 'DATA' / 'emulator_packages.json').write_text('{}')
        initialize_database()
        self.assertEqual(connection.execute("SELECT count(*) FROM migrations WHERE id LIKE '009_%'").fetchone()[0], 1)

    def test_sql_parser_supports_quoted_semicolons_and_multistatement_triggers(self):
        connection = self.connect()
        with connection:
            run_sql_safely(connection, """
                CREATE TABLE example(id INTEGER, label TEXT);
                CREATE TABLE audit(label TEXT);
                CREATE TRIGGER example_added AFTER INSERT ON example BEGIN
                    INSERT INTO audit VALUES('first;part');
                    INSERT INTO audit VALUES(NEW.label);
                END;
                INSERT INTO example VALUES(1, 'second;part');
            """)
        self.assertEqual([row[0] for row in connection.execute('SELECT label FROM audit')],
                         ['first;part', 'second;part'])
