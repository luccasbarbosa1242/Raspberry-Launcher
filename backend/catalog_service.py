"""Shared catalog rules and transactions for desktop forms, CLI and imports."""

from collections.abc import Mapping
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import sqlite3
from urllib.parse import urlsplit

from backend.database.database import Database, scoped
from backend.game_support import browser_game, require_supported_game
from backend.path_resolver import PathResolver
from backend.system.platform_detector import PlatformDetector
from contracts.catalog import CATALOG_KINDS, CatalogEntry

GAME_FIELDS = (
    'id', 'title', 'type', 'platform', 'path', 'launch_type', 'download_url',
    'archive_name', 'archive_type', 'executable', 'strip_root_folder',
    'score_enabled', 'cover_url', 'banner_url', 'logo_url',
)
VERSION_FIELDS = (
    'id', 'game_id', 'platform', 'architecture', 'path', 'launch_type',
    'download_url', 'archive_name', 'archive_type', 'executable',
    'strip_root_folder', 'score_enabled',
)
EMULATOR_FIELDS = ('id', 'name', 'plugin_id')
PACKAGE_FIELDS = (
    'id', 'emulator_id', 'system', 'architecture', 'version', 'download_url',
    'archive_type', 'executable',
)
FIELDS = dict(zip(CATALOG_KINDS, (GAME_FIELDS, VERSION_FIELDS, EMULATOR_FIELDS, PACKAGE_FIELDS)))
TABLES = dict(zip(CATALOG_KINDS, ('games', 'game_versions', 'emulators', 'emulator_packages')))
SYSTEMS = ('linux', 'windows', 'macos')
ARCHITECTURES = ('any', 'x86_64', 'aarch64', 'x86', 'armv7l')
ARCHIVES = ('zip', '7z', 'tar', 'tar.gz', 'tgz')
LAUNCH_TYPES = {
    'linux': {'linux', 'appimage', 'sh', 'python'},
    'windows': {'exe', 'python'},
    'macos': {'macos', 'app', 'sh', 'python'},
}


def _identifier(value, name='ID'):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}', value):
        raise ValueError(f'{name} inválido: use letras, números, ponto, hífen ou sublinhado.')
    return value


def _required(value, name):
    if value is None or not str(value).strip():
        raise ValueError(f'{name} é obrigatório.')
    return str(value).strip()


def _architecture(value):
    aliases = {'amd64': 'x86_64', 'x64': 'x86_64', 'arm64': 'aarch64',
               'i386': 'x86', 'i686': 'x86', 'armv7': 'armv7l'}
    value = aliases.get(value, value) or 'any'
    if value not in ARCHITECTURES:
        raise ValueError('Arquitetura inválida. Use ' + ', '.join(ARCHITECTURES) + '.')
    return value


def _boolean(value, name):
    if value in (True, 1, '1', 'true', 'True', 's', 'sim', 'yes'):
        return 1
    if value in (False, 0, None, '', '0', 'false', 'False', 'n', 'não', 'no'):
        return 0
    raise ValueError(f'{name} deve ser verdadeiro ou falso.')


def _relative_executable(value):
    value = _required(value, 'Executável')
    windows = PureWindowsPath(value)
    posix = PurePosixPath(value)
    if (windows.is_absolute() or windows.drive or posix.is_absolute() or '..' in windows.parts
            or value in ('.', '..') or value.endswith(('/', '\\'))):
        raise ValueError('O executável do pacote deve ser um caminho relativo sem "..".')
    if any(character in value for character in ('\x00', '\n', '\r')):
        raise ValueError('Caminho do executável inválido.')
    return value


def _local_file(value):
    if not value or str(value).startswith(('http://', 'https://')):
        return None
    path = Path(value).expanduser()
    path = path if path.is_absolute() else PathResolver.root() / path
    return path if path.is_file() else None


def _url(value, label='URL', local=True):
    value = _required(value, label)
    if local and value.startswith('local:'):
        source = Path(value.removeprefix('local:')).expanduser()
        source = source if source.is_absolute() else PathResolver.root() / source
        if not source.is_file():
            raise ValueError(f'{label}: arquivo local não encontrado: {source}')
        return 'local:' + str(source.resolve())
    parsed = urlsplit(value)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError(f'{label} deve usar HTTP, HTTPS ou local: sem credenciais embutidas.')
    return value


class CatalogService:
    """Catalog editing never replaces personal history or local installation rows."""

    @staticmethod
    def _kind(kind):
        if kind not in CATALOG_KINDS:
            raise ValueError('Cadastro inválido. Use game, game_version, emulator ou emulator_package.')
        return kind

    @staticmethod
    def _raw(connection, kind, record_id):
        return connection.execute(
            f'SELECT * FROM {TABLES[kind]} WHERE id = ?', (record_id,)
        ).fetchone()

    @staticmethod
    def _active(row):
        return row is not None and not (
            ('archived' in row.keys() and row['archived']) or browser_game(row)
        )

    @staticmethod
    def _entry(kind, row):
        values = {field: row[field] for field in FIELDS[kind]}
        label = row['title'] if kind == 'game' else row['name'] if kind == 'emulator' else row['id']
        return CatalogEntry(kind, row['id'], label, values)

    @scoped
    def list_records(self, kind):
        kind = self._kind(kind)
        connection = Database().connection
        rows = connection.execute(f'SELECT * FROM {TABLES[kind]} ORDER BY id').fetchall()
        return tuple(self._entry(kind, row) for row in rows if self._active(row))

    @scoped
    def get_record(self, kind, record_id):
        kind = self._kind(kind)
        row = self._raw(Database().connection, kind, record_id)
        if row is None:
            raise LookupError(f'Registro não encontrado: {record_id}')
        if not self._active(row):
            raise ValueError('Registro HTML/navegador arquivado; seu histórico foi preservado.')
        return self._entry(kind, row)

    @scoped
    def choices(self):
        connection = Database().connection
        return {
            'platforms': tuple(row['id'] for row in connection.execute(
                "SELECT id FROM platforms WHERE type IN ('native','rom') ORDER BY id"
            )),
            'emulators': tuple(row['id'] for row in connection.execute('SELECT id FROM emulators ORDER BY id')),
            'games': tuple(entry.id for entry in self.list_records('game')),
            'systems': SYSTEMS,
            'architectures': ARCHITECTURES,
        }

    def _normalize(self, connection, kind, data, existing=None, related_games=None):
        if not isinstance(data, Mapping):
            raise ValueError('O cadastro deve ser um objeto de campos e valores.')
        unknown = set(data) - set(FIELDS[kind])
        if unknown:
            raise ValueError('Campos não aceitos no cadastro: ' + ', '.join(sorted(unknown)))
        normalized = {key: existing[key] for key in FIELDS[kind]} if existing else {}
        for key, value in data.items():
            if value is not None and not isinstance(value, (str, bool, int)):
                raise ValueError(f'{key}: valor deve ser texto, número ou booleano.')
            normalized[key] = value.strip() if isinstance(value, str) else value
        for key in FIELDS[kind]:
            normalized.setdefault(key, None)
            if normalized[key] == '':
                normalized[key] = None
        normalized['id'] = _identifier(normalized['id'])
        if existing:
            if normalized['id'] != existing['id']:
                raise ValueError('O identificador de um registro existente não pode ser alterado.')
            if not self._active(existing):
                raise ValueError('Registro HTML/navegador arquivado; seu histórico foi preservado.')
        if kind in ('game', 'game_version'):
            self._normalize_game(connection, kind, normalized, existing, related_games or {})
        elif kind == 'emulator':
            normalized['name'] = _required(normalized['name'], 'Nome do emulador')
            if normalized['plugin_id']:
                _identifier(normalized['plugin_id'], 'ID do adaptador')
        else:
            self._normalize_package(connection, normalized, existing)
        return normalized

    def _normalize_game(self, connection, kind, data, existing, related_games):
        if kind == 'game':
            data['title'] = _required(data['title'], 'Título')
            data['type'] = data['type'] or 'native'
            game_type = data['type']
        else:
            data['game_id'] = _identifier(data['game_id'], 'ID do jogo')
            parent = related_games.get(data['game_id'])
            if parent is None:
                parent = self._raw(connection, 'game', data['game_id'])
            if not self._active(parent):
                raise ValueError('A versão precisa pertencer a um jogo ativo cadastrado.')
            game_type = parent['type']
            if existing and data['game_id'] != existing['game_id']:
                raise ValueError('Uma versão existente não pode ser transferida para outro jogo.')
            data['architecture'] = _architecture(data['architecture'])
        if existing:
            if kind == 'game' and data['type'] != existing['type']:
                if connection.execute('SELECT 1 FROM game_versions WHERE game_id=?', (existing['id'],)).fetchone():
                    raise ValueError('Um jogo com versões não pode trocar entre nativo e ROM; use outro ID.')
            table, column = ('game_installations', 'game_id') if kind == 'game' else (
                'game_version_installations', 'version_id'
            )
            installation = connection.execute(
                f'SELECT installed,executable_path FROM {table} WHERE {column}=?', (existing['id'],)
            ).fetchone()
            installed = existing['installed'] or _local_file(existing['path']) or (
                installation is not None and (
                    installation['installed'] or _local_file(installation['executable_path'])
                )
            )
            if installed:
                locked = ('platform', 'type') if kind == 'game' else ('platform', 'architecture')
                if any(data[name] != existing[name] for name in locked):
                    raise ValueError('Desinstale antes de alterar o sistema, a arquitetura ou o tipo de uma instalação.')
                if data['path'] and data['path'] != existing['path'] and data['download_url'] and not _local_file(data['path']):
                    raise ValueError('Preserve o caminho da instalação existente ou desinstale antes de substituí-lo.')
        require_supported_game(data)
        if game_type not in ('native', 'rom'):
            raise ValueError('Tipo de jogo inválido. Use native ou rom; jogos HTML não são suportados.')
        data['platform'] = _required(data['platform'], 'Plataforma')
        platform = connection.execute('SELECT * FROM platforms WHERE id=?', (data['platform'],)).fetchone()
        if platform is None:
            raise ValueError(f"Plataforma não cadastrada: {data['platform']}")
        if game_type == 'native':
            if data['platform'] not in SYSTEMS or platform['type'] != 'native':
                raise ValueError('Jogos nativos precisam de uma plataforma de sistema operacional.')
            data['launch_type'] = data['launch_type'] or ('exe' if data['platform'] == 'windows' else data['platform'])
            if data['launch_type'] not in LAUNCH_TYPES[data['platform']]:
                raise ValueError('Tipo de execução incompatível com o sistema operacional informado.')
        else:
            if platform['type'] != 'rom':
                raise ValueError('ROMs precisam de uma plataforma de emulação cadastrada.')
            data['launch_type'] = data['launch_type'] or 'rom'
            if data['launch_type'] != 'rom':
                raise ValueError('Uma ROM deve usar o tipo de execução rom.')
        for key in ('strip_root_folder', 'score_enabled'):
            data[key] = _boolean(data[key], key)
        if data['download_url']:
            # Editing names does not force old remote/local package links to be available now.
            if not existing or data['download_url'] != existing['download_url']:
                data['download_url'] = _url(data['download_url'], 'URL de download')
            data['archive_type'] = data['archive_type'] or 'zip'
            if data['archive_type'] not in ARCHIVES:
                raise ValueError('Formato de pacote não suportado.')
            archive = _required(data['archive_name'], 'Nome do arquivo compactado')
            if PureWindowsPath(archive).name != archive or archive in ('.', '..'):
                raise ValueError('Nome do arquivo compactado deve conter somente o nome, sem diretórios.')
            data['archive_name'] = archive
            data['executable'] = _relative_executable(data['executable'])
            if data['executable'].lower().endswith('.exe') and data['platform'] != 'windows':
                raise ValueError('Executável .exe requer a plataforma Windows.')
            data['path'] = data['path'] or (data.get('game_id') or data['id'])
        else:
            data['path'] = _required(data['path'], 'Caminho local')
            path = Path(data['path']).expanduser()
            path = path if path.is_absolute() else PathResolver.root() / path
            if not existing or data['path'] != existing['path'] or existing['download_url']:
                if not path.is_file():
                    raise ValueError(f'Caminho local não encontrado: {path}')
                data['path'] = str(path.resolve())
        require_supported_game(data)
        for name in ('cover_url', 'banner_url', 'logo_url'):
            if name in data and data[name] and (not existing or data[name] != existing[name]):
                asset = data[name]
                if not asset.startswith(('http://', 'https://', 'local:')):
                    asset = 'local:' + asset
                data[name] = _url(asset, name)

    def _normalize_package(self, connection, data, existing):
        data['emulator_id'] = _identifier(data['emulator_id'], 'ID do emulador')
        if not connection.execute('SELECT 1 FROM emulators WHERE id=?', (data['emulator_id'],)).fetchone():
            raise ValueError('Cadastre o emulador antes de adicionar seu pacote.')
        if existing and data['emulator_id'] != existing['emulator_id']:
            raise ValueError('Um pacote existente não pode ser transferido para outro emulador.')
        if data['system'] not in SYSTEMS:
            raise ValueError('Sistema operacional inválido. Use linux, windows ou macos.')
        data['architecture'] = _architecture(data['architecture'])
        data['version'] = _required(data['version'], 'Versão do pacote')
        if existing and connection.execute(
            'SELECT 1 FROM emulator_installations WHERE package_id=? AND installed=1', (existing['id'],)
        ).fetchone() and any(data[name] != existing[name] for name in ('system', 'architecture', 'version')):
            raise ValueError('Um pacote instalado deve manter sistema, arquitetura e versão; cadastre outro pacote.')
        if not existing or data['download_url'] != existing['download_url']:
            data['download_url'] = _url(data['download_url'], 'URL de download')
        else:
            data['download_url'] = _required(data['download_url'], 'URL de download')
        if data['archive_type'] not in (*ARCHIVES, 'appimage'):
            raise ValueError('Formato de pacote não suportado.')
        data['executable'] = _relative_executable(data['executable'])
        if data['archive_type'] == 'appimage' and data['system'] != 'linux':
            raise ValueError('AppImage requer o sistema Linux.')
        if data['executable'].lower().endswith('.exe') and data['system'] != 'windows':
            raise ValueError('Executável .exe requer um pacote Windows.')

    @staticmethod
    def _store(connection, table, data, updating):
        columns = tuple(data)
        if updating:
            values = {key: value for key, value in data.items() if key != 'id'}
            connection.execute(
                f'UPDATE {table} SET ' + ','.join(f'{key}=?' for key in values) + ' WHERE id=?',
                (*values.values(), data['id']),
            )
        else:
            connection.execute(
                f'INSERT INTO {table} ({",".join(columns)}) VALUES ({",".join("?" for _ in columns)})',
                tuple(data.values()),
            )

    def _write(self, connection, kind, data, existing=None, primary=True, submitted=None):
        values = dict(data)
        if kind in ('game', 'game_version'):
            if not existing:
                values['installed'] = int(not bool(data['download_url']))
            elif not data['download_url'] and (
                data['path'] != existing['path'] or data['download_url'] != existing['download_url']
            ):
                # An explicit registration of an existing local file changes local state.
                values['installed'] = 1
        self._store(connection, TABLES[kind], values, existing is not None)
        if kind == 'game':
            self._sync_assets(connection, data, existing)
            version_fields = set(VERSION_FIELDS) - {'id', 'game_id', 'architecture'}
            changed_version = not existing or any(
                name in (submitted or {}) and data[name] != existing[name]
                for name in version_fields
            )
            if primary and data['type'] == 'native' and changed_version:
                old = connection.execute(
                    'SELECT * FROM game_versions WHERE game_id=? AND platform=?',
                    (data['id'], data['platform']),
                ).fetchone()
                payload = {key: data[key] for key in version_fields}
                payload.update(id=old['id'] if old else f"{data['id']}_{data['platform']}", game_id=data['id'])
                payload['architecture'] = old['architecture'] if old else 'any'
                self._write(connection, 'game_version', payload, old)
        return self._entry(kind, self._raw(connection, kind, data['id']))

    @staticmethod
    def _sync_assets(connection, data, existing):
        for name, asset_type in (('cover_url', 'covers'), ('banner_url', 'banners'), ('logo_url', 'logos')):
            if existing and data[name] == existing[name]:
                continue
            rows = connection.execute(
                'SELECT id FROM assets WHERE game_id=? AND type=?', (data['id'], asset_type)
            ).fetchall()
            if not data[name]:
                if existing:
                    connection.execute('DELETE FROM assets WHERE game_id=? AND type=?', (data['id'], asset_type))
                continue
            asset_id = rows[0]['id'] if rows else f"{data['id']}_{asset_type}"
            connection.execute(
                '''INSERT INTO assets(id,game_id,type,remote_url,downloaded) VALUES(?,?,?,?,0)
                   ON CONFLICT(id) DO UPDATE SET remote_url=excluded.remote_url,
                   local_path=NULL,downloaded=0''',
                (asset_id, data['id'], asset_type, data[name]),
            )

    @scoped
    def save(self, kind, data, record_id=None):
        kind = self._kind(kind)
        if not isinstance(data, Mapping):
            raise ValueError('O cadastro deve ser um objeto de campos e valores.')
        connection = Database().connection
        existing = self._raw(connection, kind, record_id) if record_id is not None else None
        if record_id is not None and existing is None:
            raise LookupError(f'Registro não encontrado: {record_id}')
        if record_id is not None and 'id' not in data:
            data = dict(data, id=record_id)
        normalized = self._normalize(connection, kind, data, existing)
        if not existing and self._raw(connection, kind, normalized['id']) is not None:
            raise ValueError(f"Já existe um registro com o ID: {normalized['id']}")
        try:
            with connection:
                return self._write(connection, kind, normalized, existing, submitted=data)
        except sqlite3.IntegrityError as error:
            raise ValueError('Cadastro duplicado ou relacionamento inválido: ' + str(error)) from error

    @scoped
    def import_games(self, games):
        """Validate the entire import before writing, then commit it once."""
        if not isinstance(games, list):
            raise ValueError('A importação deve conter uma lista de jogos.')
        connection = Database().connection
        plans = []
        related = {}
        seen = set()
        for game in games:
            if not isinstance(game, Mapping):
                raise ValueError('Cada jogo importado deve ser um objeto.')
            require_supported_game(game)
            game_id = game.get('id')
            if game_id in seen:
                raise ValueError(f'ID repetido na importação: {game_id}')
            seen.add(game_id)
            data = {key: value for key, value in game.items() if key in GAME_FIELDS}
            existing = self._raw(connection, 'game', game_id)
            raw_versions = game.get('versions') or []
            if not isinstance(raw_versions, list) or any(not isinstance(item, Mapping) for item in raw_versions):
                raise ValueError('Versões devem ser uma lista de objetos.')
            for version in raw_versions:
                require_supported_game(version)
            if existing is None and raw_versions:
                # Existing JSON exports may keep package fields only on versions.
                target = data.get('platform') or PlatformDetector.current()
                primary = next((item for item in raw_versions if item.get('platform') == target), raw_versions[0])
                for key in set(GAME_FIELDS) & set(VERSION_FIELDS) - {'id'}:
                    if not data.get(key) and key in primary:
                        data[key] = primary[key]
            normalized = self._normalize(connection, 'game', data, existing)
            related[game_id] = normalized
            plans.append((game, normalized, existing, []))
        version_ids = set()
        for raw, normalized, existing, versions in plans:
            supplied = raw.get('versions') or []
            if not isinstance(supplied, list):
                raise ValueError('Versões devem ser uma lista.')
            if not supplied and normalized['type'] == 'native':
                supplied = [{key: normalized[key] for key in VERSION_FIELDS
                             if key in normalized and key != 'id'}]
            platforms = set()
            for payload in supplied:
                if not isinstance(payload, Mapping):
                    raise ValueError('Cada versão deve ser um objeto.')
                require_supported_game(payload)
                if payload.get('game_id') not in (None, normalized['id']):
                    raise ValueError('A versão importada não pertence ao jogo informado.')
                payload = {key: value for key, value in payload.items() if key in VERSION_FIELDS}
                payload['game_id'] = normalized['id']
                payload.setdefault('platform', normalized['platform'])
                if not payload.get('id'):
                    matching = connection.execute(
                        'SELECT id FROM game_versions WHERE game_id=? AND platform=?',
                        (normalized['id'], payload['platform']),
                    ).fetchone()
                    payload['id'] = matching['id'] if matching else f"{normalized['id']}_{payload['platform']}"
                version_id = payload['id']
                if version_id in version_ids or payload['platform'] in platforms:
                    raise ValueError('ID ou plataforma repetidos entre as versões importadas.')
                platforms.add(payload['platform'])
                version_ids.add(version_id)
                old = self._raw(connection, 'game_version', version_id)
                version = self._normalize(connection, 'game_version', payload, old, related)
                versions.append((version, old))
        try:
            with connection:
                for raw, data, existing, versions in plans:
                    if existing is None:
                        self._write(connection, 'game', data, primary=False)
                    for version, old in versions:
                        if old is None:
                            self._write(connection, 'game_version', version)
        except sqlite3.IntegrityError as error:
            raise ValueError('Importação cancelada: ' + str(error)) from error
        return tuple(self._entry('game', self._raw(connection, 'game', data['id'])) for _, data, _, _ in plans)
