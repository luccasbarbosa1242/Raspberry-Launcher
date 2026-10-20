"""Catalog edits exercise the same persistence paths used by forms and CLI."""

from dataclasses import asdict
import json
import os
import subprocess
import sys

from backend.catalog_service import CatalogService
from tests.support import BackendCase, PROJECT


class CatalogServiceTests(BackendCase):
    def setUp(self):
        super().setUp()
        self.catalog = CatalogService()
        self.local = self.home / 'local.py'
        self.local.write_text("print('local game')\n", encoding='utf-8')

    def game(self, game_id='catalog_game', **fields):
        data = dict(id=game_id, title='Catalog game', type='native', platform='linux',
                    path=str(self.local), launch_type='python')
        data.update(fields)
        return data

    def package(self, package_id='test_package', **fields):
        data = dict(id=package_id, emulator_id='custom_emulator', system='linux',
                    architecture='x86_64', version='1.0', download_url='https://example.org/emulator.zip',
                    archive_type='zip', executable='emulator')
        data.update(fields)
        return data

    def cli(self, *arguments, data=None, expected=0):
        result = subprocess.run(
            [sys.executable, '-m', 'backend', '--home', str(self.home), *arguments],
            cwd=PROJECT, env=os.environ.copy(), input=json.dumps(data) if data is not None else None,
            text=True, capture_output=True, timeout=20,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_create_and_partial_edit_preserve_personal_state_and_installation(self):
        created = self.catalog.save('game', self.game())
        self.assertEqual(created.values['title'], 'Catalog game')
        db = self.connection()
        db.execute("UPDATE games SET favorite=1,play_time=84,last_played='2026-10-20' WHERE id=?", (created.id,))
        db.commit()
        self.catalog.save('game', {'title': 'Renamed'}, record_id=created.id)
        row = db.execute('SELECT * FROM games WHERE id=?', (created.id,)).fetchone()
        self.assertEqual((row['favorite'], row['play_time'], row['last_played']), (1, 84, '2026-10-20'))
        self.assertEqual(row['path'], str(self.local))
        versions = db.execute('SELECT * FROM game_versions WHERE game_id=?', (created.id,)).fetchall()
        self.assertEqual(len(versions), 1)
        self.assertEqual(versions[0]['id'], 'catalog_game_linux')
        self.assertEqual(versions[0]['installed'], 1)

    def test_edit_main_package_preserves_other_platform_version_and_ids(self):
        self.catalog.save('game', self.game())
        windows = self.catalog.save('game_version', dict(
            id='custom_windows', game_id='catalog_game', platform='windows', architecture='amd64',
            path='catalog_game', launch_type='exe', download_url='https://example.org/windows.zip',
            archive_name='windows.zip', archive_type='zip', executable='game.exe',
        ))
        self.assertEqual(windows.values['architecture'], 'x86_64')
        self.catalog.save('game', dict(title='Updated', score_enabled=True), record_id='catalog_game')
        versions = self.catalog.list_records('game_version')
        self.assertEqual({item.id for item in versions}, {'catalog_game_linux', 'custom_windows'})
        self.assertEqual(self.catalog.get_record('game_version', 'custom_windows').values, windows.values)
        with self.assertRaisesRegex(ValueError, 'identificador'):
            self.catalog.save('game', {'id': 'another'}, record_id='catalog_game')

    def test_game_download_registration_does_not_require_downloading(self):
        game = self.game(path='', launch_type='linux', download_url='https://example.org/game.zip',
                         archive_name='game.zip', archive_type='zip', executable='bin/game')
        entry = self.catalog.save('game', game)
        self.assertEqual(entry.values['path'], 'catalog_game')
        self.assertFalse((self.home / 'installed/catalog_game').exists())
        self.assertEqual(self.connection().execute(
            "SELECT installed FROM games WHERE id='catalog_game'"
        ).fetchone()[0], 0)

    def test_download_registration_can_be_changed_to_an_existing_local_installation(self):
        self.catalog.save('game', self.game(path='', launch_type='python',
                          download_url='https://example.org/game.zip', archive_name='game.zip',
                          archive_type='zip', executable='local.py'))
        self.catalog.save('game', {'download_url': None, 'path': str(self.local)}, record_id='catalog_game')
        db = self.connection()
        self.assertEqual(db.execute("SELECT installed FROM games WHERE id='catalog_game'").fetchone()[0], 1)
        self.assertEqual(db.execute("SELECT installed FROM game_versions WHERE game_id='catalog_game'").fetchone()[0], 1)

    def test_clearing_a_download_cannot_fabricate_a_missing_local_installation(self):
        self.catalog.save('game', self.game(path='', launch_type='python',
                          download_url='https://example.org/game.zip', archive_name='game.zip',
                          archive_type='zip', executable='local.py'))
        with self.assertRaisesRegex(ValueError, 'Caminho local'):
            self.catalog.save('game', {'download_url': None}, record_id='catalog_game')
        self.assertEqual(self.catalog.get_record('game', 'catalog_game').values['download_url'],
                         'https://example.org/game.zip')

    def test_installed_game_version_cannot_change_target_without_uninstalling(self):
        self.catalog.save('game', self.game())
        with self.assertRaisesRegex(ValueError, 'Desinstale'):
            self.catalog.save('game_version', {'architecture': 'aarch64'}, record_id='catalog_game_linux')
        with self.assertRaisesRegex(ValueError, 'Desinstale'):
            self.catalog.save('game', {'platform': 'windows', 'launch_type': 'python'}, record_id='catalog_game')

    def test_separate_installation_state_also_locks_the_version_target(self):
        self.catalog.save('game', self.game(path='', launch_type='python',
                          download_url='https://example.org/game.zip', archive_name='game.zip',
                          archive_type='zip', executable='local.py'))
        db = self.connection()
        db.execute("UPDATE game_version_installations SET installed=1,executable_path=? WHERE version_id='catalog_game_linux'",
                   (str(self.local),))
        db.commit()
        with self.assertRaisesRegex(ValueError, 'Desinstale'):
            self.catalog.save('game_version', {'architecture': 'aarch64'}, record_id='catalog_game_linux')

    def test_rom_uses_existing_platform_without_claiming_adapter_support(self):
        rom = self.home / 'game.iso'
        rom.write_bytes(b'test rom fixture')
        entry = self.catalog.save('game', self.game('rom_local', type='rom', platform='ps2',
                                                  launch_type='rom', path=str(rom)))
        self.assertEqual(entry.values['type'], 'rom')
        self.assertFalse(self.catalog.list_records('game_version'))

    def test_emulator_and_package_edits_keep_installation_and_stable_relationships(self):
        self.catalog.save('emulator', dict(id='custom_emulator', name='Custom', plugin_id='future_adapter'))
        db = self.connection()
        db.execute("UPDATE emulators SET installed=1,executable_path=?,version='old' WHERE id='custom_emulator'",
                   (str(self.local),))
        db.commit()
        before = dict(db.execute("SELECT * FROM emulator_installations WHERE emulator_id='custom_emulator'").fetchone())
        self.catalog.save('emulator', {'name': 'Renamed'}, record_id='custom_emulator')
        package = self.catalog.save('emulator_package', self.package())
        self.catalog.save('emulator_package', {'version': '2.0'}, record_id=package.id)
        after = dict(db.execute("SELECT * FROM emulator_installations WHERE emulator_id='custom_emulator'").fetchone())
        self.assertEqual(before, after)
        self.assertEqual(self.catalog.get_record('emulator_package', package.id).values['emulator_id'], 'custom_emulator')
        self.assertEqual(self.catalog.get_record('emulator', 'custom_emulator').values['plugin_id'], 'future_adapter')

    def test_relationship_system_architecture_and_package_paths_are_validated(self):
        self.catalog.save('emulator', {'id': 'custom_emulator', 'name': 'Custom'})
        for fields in (
            dict(emulator_id='missing'), dict(system='ps2'), dict(architecture='mips'),
            dict(executable='../outside'), dict(executable='/absolute'),
            dict(executable='C:\\outside.exe'), dict(executable='emulator.exe'),
            dict(download_url='ftp://example.org/a.zip'),
            dict(download_url='https://user:secret@example.org/a.zip'),
            dict(archive_type='unsupported'),
        ):
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                self.catalog.save('emulator_package', self.package(**fields))
        self.assertFalse(self.catalog.list_records('emulator_package') and any(
            row.id == 'test_package' for row in self.catalog.list_records('emulator_package')
        ))
        self.assertEqual(self.catalog.save('emulator_package', self.package(architecture='armv7')).values['architecture'], 'armv7l')

    def test_installed_package_cannot_change_owner_or_target(self):
        self.catalog.save('emulator', dict(id='custom_emulator', name='Custom'))
        self.catalog.save('emulator', dict(id='another_emulator', name='Another'))
        self.catalog.save('emulator_package', self.package())
        db = self.connection()
        db.execute("UPDATE emulator_installations SET package_id='test_package',installed=1 WHERE emulator_id='custom_emulator'")
        db.commit()
        for data in ({'emulator_id': 'another_emulator'}, {'architecture': 'aarch64'},
                     {'system': 'windows'}, {'version': '2.0'}):
            with self.subTest(data=data), self.assertRaises(ValueError):
                self.catalog.save('emulator_package', data, record_id='test_package')
        self.assertEqual(self.catalog.get_record('emulator_package', 'test_package').values['emulator_id'], 'custom_emulator')
        self.assertEqual(db.execute("SELECT emulator_id FROM emulator_installations WHERE package_id='test_package'").fetchone()[0], 'custom_emulator')

    def test_invalid_game_id_platform_paths_and_readonly_fields_are_rejected(self):
        for fields in (
            dict(id='../bad'), dict(id=''), dict(platform='unknown'),
            dict(platform='ps2'), dict(launch_type='exe'), dict(path='missing.py'),
            dict(installed=1), dict(favorite=1), dict(play_time=100),
        ):
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                self.catalog.save('game', self.game(**fields))
        self.assertFalse(self.catalog.list_records('game'))

    def test_browser_execution_is_rejected_even_for_native_and_game_versions(self):
        for fields in (
            dict(launch_type='html'), dict(type='web'), dict(platform='web'),
            dict(path='https://example.org/game'), dict(path='/tmp/game.HTML?play=1'),
        ):
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                self.catalog.save('game', self.game(**fields))
        self.catalog.save('game', self.game())
        with self.assertRaises(ValueError):
            self.catalog.save('game_version', dict(id='browser_version', game_id='catalog_game',
                              platform='windows', path='https://example.org/game', launch_type='html'))
        self.assertEqual(len(self.catalog.list_records('game_version')), 1)

    def test_import_validates_all_records_before_inserting_anything(self):
        good = self.game('first')
        bad = self.game('second', launch_type='html')
        with self.assertRaises(ValueError):
            self.catalog.import_games([good, bad])
        self.assertFalse(self.catalog.list_records('game'))
        bad = self.game('second')
        bad['versions'] = [dict(id='bad_version', platform='linux', path='https://example.org/game', launch_type='html')]
        with self.assertRaises(ValueError):
            self.catalog.import_games([good, bad])
        self.assertFalse(self.catalog.list_records('game'))

    def test_import_is_idempotent_and_does_not_overwrite_edited_catalog_or_history(self):
        payload = self.game()
        result = self.catalog.import_games([payload])
        self.assertEqual(len(result), 1)
        self.catalog.save('game', {'title': 'Locally renamed'}, record_id='catalog_game')
        db = self.connection()
        db.execute("UPDATE games SET favorite=1,play_time=333 WHERE id='catalog_game'")
        db.commit()
        self.catalog.import_games([payload])
        game = self.catalog.get_record('game', 'catalog_game')
        self.assertEqual(game.values['title'], 'Locally renamed')
        self.assertEqual(len(self.catalog.list_records('game_version')), 1)
        self.assertEqual(db.execute("SELECT favorite,play_time FROM games WHERE id='catalog_game'").fetchone()[:], (1, 333))

    def test_import_accepts_packages_on_versions_and_preserves_their_explicit_identifiers(self):
        payload = dict(id='versioned_game', title='Versioned', type='native', versions=[dict(
            id='stable_package_identity', platform='linux', path='versioned_game', launch_type='linux',
            download_url='https://example.org/game.zip', archive_name='game.zip',
            archive_type='zip', executable='game',
        )])
        self.catalog.import_games([payload])
        self.assertEqual(self.catalog.get_record('game', 'versioned_game').values['platform'], 'linux')
        self.catalog.import_games([payload])
        # A later seed omitting explicit versions must retain the recorded identity too.
        existing = self.catalog.get_record('game', 'versioned_game').values
        self.catalog.import_games([existing])
        self.assertEqual([entry.id for entry in self.catalog.list_records('game_version')], ['stable_package_identity'])

    def test_cli_and_service_share_records_validation_and_errors(self):
        response = self.cli('catalog', 'save', 'game', '--file', '-', data=self.game())
        created = json.loads(response.stdout)
        self.assertEqual(created, asdict(self.catalog.get_record('game', 'catalog_game')))
        edited = json.loads(self.cli('catalog', 'save', 'game', '--file', '-', '--edit', 'catalog_game',
                                    data={'title': 'CLI edit'}).stdout)
        self.assertEqual(edited['values']['title'], 'CLI edit')
        listed = json.loads(self.cli('catalog', 'list', 'game').stdout)
        self.assertEqual(listed, [edited])
        response = self.cli('catalog', 'save', 'game', '--file', '-',
                            data=self.game('bad_cli', launch_type='html'), expected=1)
        self.assertIn('HTML', response.stderr)
        self.assertFalse(self.connection().execute("SELECT 1 FROM games WHERE id='bad_cli'").fetchone())

    def test_cli_atomic_import_rejects_browser_versions(self):
        response = self.cli('catalog', 'import', '--file', '-',
                            data=[self.game(), self.game('bad', launch_type='html')], expected=1)
        self.assertIn('HTML', response.stderr)
        self.assertFalse(self.catalog.list_records('game'))
