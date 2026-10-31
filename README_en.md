<div align="center">

# 🚀 Launcher PI

🌎 Language:

* 🇺🇸 English (Current)
* 🇧🇷 [Versão em Português](README.md)

### Game Launcher built with Python, CustomTkinter and SQLite

Centralize native games and ROMs into a single library.

### 📈 Development Status

> **Phases 1 and 2 completed • Local profiles and online accounts available • Phase 3: Downloads, Emulators and ROMs next**

<img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/CustomTkinter-UI-green?style=for-the-badge" />
<img src="https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/Status-Under%20Development-orange?style=for-the-badge" />

<img src="https://img.shields.io/badge/Linux-Supported-success?style=for-the-badge" />
<img src="https://img.shields.io/badge/Windows-Supported-success?style=for-the-badge" />
<img src="https://img.shields.io/badge/Open%20Source-Yes-blue?style=for-the-badge" />

</div>

---

# 📖 About the Project

**Launcher PI** is a game launcher built with **Python**, using **CustomTkinter** for the graphical interface and **SQLite** for local data and **Supabase Auth + PostgreSQL** for optional online accounts and personal-stat synchronization.

The project aims to centralize different types of games into a single library, allowing users to install, organize and launch their games through a modern and intuitive interface.

Launcher PI currently supports:

* 🎮 Native Games
* 🕹️ ROMs
* ⚙️ Emulators

Everything is managed from a single application.

---

## 🎯 Project Philosophy

Launcher PI has been designed around a few core principles since the beginning of development:

* Modular architecture
* Decoupled codebase
* Database-driven design
* Automated installation workflow
* Plugin-based expansion
* Linux and Windows compatibility
* Easy game registration without modifying the source code

The long-term goal is to allow new games to be added simply by inserting records into the database, eliminating the need to modify the launcher itself.

---

# ⚠️ Important Notice

> [!CAUTION]
>
> ## 🔴 PROTECT YOUR DATA BEFORE MIGRATING
>
> **Phase 1 (T00, T01, T03 and T05)** consolidated catalog data in SQLite. **Phase 2** added local profiles, persistent preferences, authentication and optional account synchronization.
>
> `games.py` is already absent from execution. JSON files remain for initial data, import/export and plugin descriptors.
>
> Migrations preserve existing records; do not recreate an empty database to update. HTML/browser games are archived and removed from the active catalog. Google Drive and `gdown` remain available for downloads.
>
> Before changing data, read [Phase 1](docs/FASE1.md), [Phase 2](docs/FASE2.md), [Online accounts](docs/CONTAS_ONLINE.md) and [Recovery](docs/RECUPERACAO.md). These detailed documents are in Portuguese. Online synchronization **does not** back up ROMs, saves or installations.

---

# 🎯 Current Priorities

> This section reflects the current focus of development.

---

# 🔴 Highest Priority

## Phase 3 — Downloads, Emulators and ROMs (next phase)

* [x] Existing download, installation, version and plugin infrastructure preserved
* [x] Emulator and package catalogs managed through SQLite
* [x] Existing automated download, installation and uninstall tests
* [ ] Verify real emulator packages per operating system and architecture
* [ ] Complete emulator detection, installation and automatic configuration
* [ ] Validate end-to-end ROM launching, one adapter at a time
* [ ] Cover download integrity, failures, recovery and real compatibility

---

## Database — Phase 1 (completed)

* [x] SQLite structure
* [x] Migration system
* [x] Persistent database
* [x] Library integration
* [x] GameRepository
* [x] LibraryManager
* [x] AssetRepository
* [x] GameVersionRepository
* [x] Game registration tools
* [x] Game update tools
* [x] Game removal tools
* [x] Asset registration
* [x] Game version management
* [x] Runtime platform records queried from the database
* [x] Emulator catalog and package records queried from the database
* [x] `games.py` absent from execution

---

## Game System (92%)

* [x] Native games
* [x] HTML/browser support removed with legacy history archived
* [x] Dynamic library
* [x] Automatic downloads
* [x] Automatic installation
* [x] Automatic uninstallation
* [x] Database-driven updates
* [x] Administrative registration tools
* [x] Multi-platform game versions (Linux / Windows)
* [x] Individual game pages

---

## Emulators (65% — existing infrastructure; Phase 3 integration pending)

* [x] Core architecture
* [x] EmulatorManager
* [x] PackageResolver
* [x] PluginLoader
* [x] PluginRegistry
* [x] RomLauncher
* [x] Download architecture
* [ ] Real emulator downloads
* [ ] Fully automated installation
* [ ] Complete ROM integration
* [ ] Emulator library

---

# 🟠 High Priority

## User Interface (80%)

* [x] Functional game library
* [x] Game card system
* [x] Standardized covers
* [x] Covers loaded through AssetManager
* [x] Database-integrated home page
* [x] Visual installation status
* [x] Favorites, Recent and Search views connected to the backend
* [x] Visual feedback for installation and removal stages
* [x] Individual game pages
* [ ] Collections system
* [ ] Final UI improvements
* [x] Visual download feedback

---

## Assets (90%)

* [x] AssetManager
* [x] AssetRepository
* [x] Local cache
* [x] Remote assets
* [x] Local assets
* [x] Fallback system
* [x] Administrative tools
* [ ] Screenshots
* [ ] Background images
* [ ] Custom icons

---

## HTML and Browser Games

* [x] Removed from registration, import, active catalog and execution
* [x] Legacy history preserved through archiving
* [x] File downloads over HTTP and Google Drive preserved

---

# 🟡 Medium Priority

## Library

* [x] Individual game pages
* [ ] Description
* [ ] Developer
* [ ] Genre
* [ ] Release year
* [x] Play time
* [ ] Update history

---

## Content

* [ ] Add more games
* [ ] Add more emulators
* [ ] Add more plugins
* [ ] Add more platforms

---

# 🟢 Low Priority

## Settings

* [x] Light and dark themes, with an option to follow the system
* [x] Per-profile persistent theme preference
* [ ] Background music
* [x] Music volume **preference** (not actual audio playback or system volume control)
* [ ] Brightness control

---

## Users

* [x] Independent local profiles and optional online accounts
* [x] Per-profile favorites, play time and recently played games
* [x] Account statistics and preference synchronization
* [x] Supabase/Brevo email signup, confirmation and login
* [x] **Remember me** through the OS credential vault; no saved password
* [ ] End-to-end synchronization check on two physical computers
* [ ] Full cloud backup of files and settings

---

## Distribution

* [ ] Official installer
* [ ] Automatic updater
* [ ] Digital signature
* [ ] Official distribution

---

# 🔵 Future Ideas

* [ ] Achievement system
* [ ] Cloud backup
* [x] Personal stats/preference sync implemented (two-computer physical test pending)
* [ ] Theme marketplace
* [ ] Mod support
* [ ] Assisted local multiplayer
* [ ] Public plugin API

---

# ✨ Features

## 🎮 Native Games

* Automatic installation
* Automatic downloads
* SQLite-based registration
* Integrated launcher
* Linux support
* Windows support
* Multiple versions per game

---

## 🌐 HTML and Browser Games

* Support removed in Phase 1
* Legacy records preserved as archived history
* New registrations and imports of this game mode are rejected

Google Drive and `gdown` remain available for file downloads. The removal applies to running games in a browser.

---

## 🕹️ ROMs & Emulators

* ROM-ready architecture
* Plugin system
* Automatic emulator downloads (under development)
* Multi-emulator support
* Expansion-ready architecture

---

## 📚 Library

* Dynamic game library
* Database-driven registration
* Score system
* Favorites
* Play history
* Centralized management

---

## 👤 Local Profiles and Online Accounts — Phase 2

* Separate local profiles with independent favorites, play time, recent games and themes
* Supabase Auth, Brevo SMTP email verification and real user login tested
* Manual and periodic automatic personal-stat/preference syncing with a local offline queue and idempotent retries
* Optional one-time import from the default local profile without deleting its data
* Optional **Remember me** using a renewable session token in the OS credential vault; passwords are never stored
* Installed games, emulator binaries, ROMs, saves and catalogs remain **local**
* Automated multi-device simulation passed; validation on two physical computers is still pending

Documentation: [Local profiles](docs/FASE2.md) and [Online accounts](docs/CONTAS_ONLINE.md) (in Portuguese).

---

## 🖼️ Assets

* AssetManager
* AssetRepository
* Intelligent cache
* Remote covers
* Local covers
* Fallback system
* Automatic updates
* Administrative tools

---

# 🆕 Project Updates — Phases 1 and 2

> **Phase 1: recoverable baseline and consolidated catalog • Phase 2: profiles, online accounts and sync • Phase 3: preparation**

## ✅ Phase 1 Deliverables (preserved)

* [x] **T00:** identified baseline, consistent backup and temporary restore rehearsal
* [x] **T01:** consolidated database catalog, versioned migrations and separate local installations
* [x] **T03:** shared services for adding/editing games, versions, emulators and packages through desktop forms and CLI
* [x] **T05:** archived HTML/browser games and blocked registration, import and execution

* [x] Graphical interface isolated in `frontend/`
* [x] Game logic, database, downloads, installation and emulators concentrated in `backend/`
* [x] Actions, navigation and background tasks coordinated by `application/`
* [x] Communication between layers defined through data and interfaces in `contracts/`
* [x] Application composition and implementation wiring centralized in `main.py`
* [x] Backend without UI imports and frontend without backend imports
* [x] UI preview using demonstration data without loading the backend
* [x] Backend CLI for operation without the graphical interface
* [x] Dependencies separated into `requirements/frontend.txt` and `requirements/backend.txt`
* [x] Administrative tools preserved in `backend/tools/`
* [x] Provided SQLite database, covers, banners, scores and configuration preserved
* [x] Tests covering architecture, backend, application, downloads, UI and administrative tools

## ✅ Phase 2 Deliverables

* [x] `012_local_profiles.sql` and `013_online_accounts.sql` migrations without deleting existing data
* [x] Per-profile favorites, play time, recent games, preferences and themes
* [x] Supabase Auth signup/login, PostgreSQL RLS policies and Brevo email confirmation
* [x] Manual/periodic sync, offline queue, idempotent events and optional local-history import
* [x] Optional persistent session with `keyring` and explicit logout
* [x] 143 passing tests on `main`, including GUI, PostgreSQL and backup restoration
* [ ] Validate synchronization on two physical computers

---

## 📂 Layer Responsibilities

| Folder / File | Responsibility |
| --------------- | ----------------------- |
| `frontend/` | Windows, screens, cards, styles, rendered images and widget state |
| `backend/` | Application rules, SQLite, profiles, online accounts, synchronization, downloads, installation, uninstallation, launching and emulators |
| `application/` | Action coordination, navigation, background tasks and UI updates |
| `contracts/` | Shared data and public interfaces used by the layers |
| `main.py` | Application startup and wiring of concrete implementations |
| `backend/tools/` | Administrative command-line tools |
| `backend/online.py`, `backend/secure_session.py` | Authentication, personal sync and optional OS-vault session persistence |
| `ASSETS/`, `DATA/`, `USERDATA/` | Project resources and data |

The interface sends actions containing identifiers and receives data ready for display. Widgets are never passed to the backend, and screens do not run SQL queries, downloads or installations.

---

## 🛠️ Included Fixes

* [x] Download calls compatible with `gdown 6.1.0`, removing the unsupported `fuzzy` argument
* [x] Asset downloads and game installation using the corrected download call
* [x] **Uninstall** action preserved in the three-dot menu for installed games
* [x] Uninstall availability fixed for local games and ROMs, including those outside the managed installation folder
* [x] Managed installation removal and record updates without deleting external executables or ROM files

---

## ▶️ Running Each Layer

From the project directory, using Python 3.12 and the required dependencies.

**Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

**Windows (PowerShell):**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

If PowerShell blocks activation, adjust the execution policy for the **current process only**. Use the activated environment's Python instead of mixing incompatible Python installations. Set `RASPBERRY_LAUNCHER_HOME` to a separate data directory if desired; **do not overwrite the existing database**.

Online accounts use the project's HTTPS URL and public Supabase key in `backend/online_defaults.py`. Set `RASPBERRY_ONLINE_DISABLED=1` to use local profiles only. **Remember me** requires an available secure OS credential vault. Never commit user passwords, SMTP secrets or service-role keys.

Independent UI preview and administrative CLI:

```bash
python -m frontend.preview
python -m backend --help
python -m backend list
python -m backend catalog --help
```

Desktop registration forms live in the sidebar's **Cadastros** section. Adding an emulator/package record does not implement its adapter or guarantee ROM execution. See [Phase 1](docs/FASE1.md).

Linux validation with a virtual display:

```bash
xvfb-run -a python -m unittest discover -s tests -v
python -m compileall -q backend frontend application contracts tests main.py
ruff check .
```

CI also runs PostgreSQL 16 security checks and recovery rehearsals. For data migration, follow [Recovery](docs/RECUPERACAO.md).

---

## 🧪 Update Validation

* [x] **143 automated tests** passed on `main` ([GitHub Actions run](https://github.com/luccasbarbosa1242/Raspberry-Launcher/actions/runs/39707210299))
* [x] Python compilation, Ruff, dependencies, PostgreSQL 16 RLS/security and recovery rehearsal passed
* [x] Actual email registration, Brevo confirmation and online login verified; **Remember me** tested on Windows
* [x] Historical restructuring check: 27 data/resource files compared byte-for-byte with the original ZIP
* [ ] Real sync test on two physical computers and end-to-end emulator/ROM validation in Phase 3

Multi-device synchronization and network-error tests use a deterministic simulated server. Download tests use local files and controlled HTTP; not every external link or platform has been validated.

Details: [Architecture](docs/ARQUITETURA.md), [Analysis](docs/ANALISE_E_MUDANCAS.md), [Phase 2](docs/FASE2.md) and [Online accounts](docs/CONTAS_ONLINE.md) (in Portuguese).

---

# ⚙️ Internal Architecture

Launcher PI was designed around a modular architecture where every component has a single responsibility.

The project separates UI code in `frontend/`, application rules in `backend/`, coordination in `application/` and shared interfaces in `contracts/`. The `main.py` entry point connects their concrete implementations.

The application is currently composed of five major subsystems:

* Library
* Installation
* Assets
* Launchers
* Emulators

---

# 📚 Library System

The Library System is the heart of Launcher PI.

Almost every screen displayed by the application retrieves its information through this module.

Current flow:

```text
User Interface
      │
      ▼
LauncherController
      │
      ▼
LauncherService
      │
      ▼
LibraryManager
      │
      ▼
GameRepository
      │
      ▼
SQLite Database
```

The `LibraryManager` handles library queries in the backend. The UI receives results through `LauncherController`, `LauncherService` and the data types defined in `contracts/`.

Its responsibilities include:

* Listing games
* Searching games
* Retrieving installed games
* Managing favorites
* Updating installation status
* Registering play time
* Providing game metadata

The UI never communicates directly with SQLite.

---

# 🎮 Game Version System

Each game may have one or more platform-specific versions.

Example:

```text
Snake

├── Linux
└── Windows
```

These versions are stored inside the:

```text
game_versions
```

table.

Every version contains its own:

* Download URL
* Archive name
* Executable
* Launch type
* Platform
* Installation status

Architecture:

```text
Game
     │
     ▼
GameVersionManager
     │
     ▼
GameVersionRepository
     │
     ▼
game_versions
```

This allows a single game entry to support multiple operating systems without duplicating game records.

---

# 📦 Installation System

Every installation is handled by the `NativeGameInstaller`.

Installation workflow:

```text
Install Button
        │
        ▼
LauncherController
        │
        ▼
LauncherService
        │
        ▼
NativeGameInstaller
        │
        ▼
GameVersionManager
        │
        ▼
game_versions
        │
        ▼
Download
        │
        ▼
Extraction
        │
        ▼
Database Update
```

After installation the launcher automatically updates:

* executable path;
* installation status;
* installed version;
* game library.

The long-term goal is to make the installation process completely database-driven.

---

# 🖼️ Asset Management System

Asset retrieval and caching belong to the backend; the frontend renders images using the resolved file paths it receives.

Every asset passes through the Asset Management pipeline.

Architecture:

```text
Game Card
      │
      ▼
LauncherController
      │
      ▼
LauncherService
      │
      ▼
AssetManager
      │
      ▼
AssetRepository
      │
      ▼
assets Table
      │
      ▼
Local Cache
      │
      ▼
Rendered Image
```

Whenever an asset is requested:

1. The launcher checks the local cache.
2. If the file exists, it is loaded immediately.
3. Otherwise, it downloads (or copies) the asset.
4. The cache is updated.
5. The database is updated.
6. The interface displays the image.

If no image is available, a fallback placeholder is automatically used.

---

# 🚀 Launcher System

Launcher PI uses a launcher factory pattern.

This allows the interface to launch any game without knowing how that game should actually be executed.

Architecture:

```text
Game
    │
    ▼
LauncherFactory
    │
    ├────────► NativeLauncher
    │
    └────────► RomLauncher
```

Every game launch request goes through the `LauncherFactory`.

The factory decides which launcher should be used according to the game type.

---

## NativeLauncher

Responsible for launching:

* Native Linux games
* Native Windows games
* Installed executables
* Local applications

Its only responsibility is to locate the executable and launch it.

---

## RomLauncher

Responsible for:

* Locating the correct emulator
* Locating the ROM
* Launching both together

Its full implementation is currently under development.

---

# 🔌 Plugin System

Every emulator integration was designed to work through plugins.

Architecture:

```text
PluginLoader
      │
      ▼
PluginRegistry
      │
      ▼
Plugin
```

Every plugin will eventually be able to define:

* Installation logic
* Update logic
* Executable detection
* Launch arguments
* Supported ROM formats
* Emulator-specific configuration

This architecture allows Launcher PI to support new emulators without modifying its core code.

---

# 🕹️ Emulator System

Emulators are managed by the `EmulatorManager`.

Planned execution flow:

```text
RomLauncher
      │
      ▼
EmulatorManager
      │
      ▼
PackageResolver
      │
      ▼
Plugin
      │
      ▼
Download
```

The final objective is for users to never install emulators manually.

If an emulator is missing, Launcher PI will:

* detect the missing emulator;
* download it automatically;
* install it;
* register it in the database;
* launch the game.

---

# 🗄️ Database Design

Launcher PI currently separates responsibilities across multiple tables.

---

## games

Stores general information about every registered game.

Examples:

* Title
* Type
* Main platform
* Favorites
* Installation status
* Play time

---

## game_versions

Stores platform-specific versions.

Example:

```text
snake_linux
snake_windows
```

Each version stores:

* Download URL
* Archive
* Executable
* Platform
* Installation status

---

## assets

Stores every visual asset.

Including:

* Covers
* Banners
* Logos

Each asset stores:

* Remote source
* Cached file
* Download status

---

## Consolidated Database Tables

The database already includes these catalog and collection tables:

```text
platforms
```

Stores every supported gaming platform.

---

```text
emulators
```

Stores emulator catalog records. Packages live in `emulator_packages`; local installations live in `emulator_installations`.

---

```text
collections
```

Stores user-created collections.

---

```text
game_collections
```

Associates games with collections.

---

# 🔄 Complete Launcher Flow

```text
User
      │
      ▼
User Interface
      │
      ▼
LauncherController
      │
      ▼
LauncherService
      │
      ▼
LibraryManager
      │
      ▼
SQLite Database
      │
      ▼
LauncherFactory
      │
      ├──────────────► NativeLauncher
      │                     │
      │                     ▼
      │              NativeGameInstaller
      │                     │
      │                     ▼
      │             GameVersionManager
      │                     │
      │                     ▼
      │              game_versions
      │
      └──────────────► RomLauncher
                            │
                            ▼
                     EmulatorManager
                            │
                            ▼
                      PluginLoader
                            │
                            ▼
                           Plugin
                            │
                            ▼
                            ROM
```

---

# 💡 Architectural Goals

Launcher PI was designed so that adding a new game eventually becomes a simple administrative task.

The expected workflow is:

1. Register the game in the database.
2. Register one or more platform-specific versions.
3. Register the game assets.
4. Launch the application.

No source code modifications should be required.

This architecture makes Launcher PI highly scalable and significantly simplifies future maintenance and expansion.

---

# 🎯 Final Goal

Launcher PI aims to become a complete game management platform, providing a simple, modern and highly automated experience.

When development is complete, users will be able to manage:

* 🎮 Native Games
* 🕹️ ROMs
* ⚙️ Emulators
* 🖼️ Game Assets
* 📚 Unified Game Library

—all from a single application.

The long-term vision is to make Launcher PI entirely database-driven, allowing new games to be added without modifying the application's source code.

---

# 🗺️ Development Roadmap

## ✅ Phase 1 — Baseline, Catalog Editing and Supported Games

Phase 1 was completed with **T00, T01, T03 and T05** on the existing modular architecture:

* Identified baseline, consistent recovery point and temporary restore rehearsal
* Safe migrations and consolidated game, platform, emulator and package records
* Separate package/version catalog data and local installations
* Desktop forms and CLI using the same registration/editing services and validation
* Archived HTML/browser games, blocked from new registration, import and execution
* Preserved action menu, uninstallation, native games, existing ROM flows and Google Drive downloads
* Preserved `frontend`, `backend`, `application` and `contracts` boundaries

`games.py` was already absent from execution. Current migration details, results and practical limits are in [Phase 1](docs/FASE1.md) and [Validation](docs/VALIDACAO.md).

---

## ✅ Phase 2 — Profiles, Preferences and Online Accounts (Completed)

Delivered independent local profiles, individual favorites/play time, persistent preferences, Supabase Auth login with Brevo email verification, optional personal-stat synchronization, offline event queue, local-history import and secure **Remember me**. Real signup/login and session persistence were verified, and **143 automated tests** passed on `main`. **Pending acceptance test:** synchronize between two physical computers. See [Phase 2](docs/FASE2.md) and [Online accounts](docs/CONTAS_ONLINE.md).

---

## 🚧 Phase 3 — Downloads, Emulators and ROMs (Next Phase)

Build on existing download/installation/version/plugin infrastructure to finish real emulator packages, OS/architecture detection, configuration, failure recovery and end-to-end ROM launching, validating each platform and adapter separately. Registering an emulator alone does **not** guarantee compatibility.

---

## 🚀 Phase 4 — RGSX Integration

Query and synchronize the **external RGSX catalog**, then connect downloads and ROM launching on supported platforms. **Account/statistics synchronization** is already part of Phase 2 and is separate from RGSX. Local profiles, personal statistics and basic themes are complete; actual music playback, achievements, advanced library pages and system controls remain future work.

---

# 📚 Development Philosophy

Launcher PI follows a few core software engineering principles throughout its development.

## Modular Design

Every module has a single responsibility.

This makes the project easier to maintain, test and expand over time.

---

## Database-Driven Architecture

The database is responsible for storing nearly every piece of information used by the launcher.

This includes:

* Games
* Game versions
* Assets
* Installation status
* Favorites
* Play time

The database also stores:

* Platforms
* Emulator catalog and packages
* Collections
* Local game and emulator installations

Local profiles, online accounts and personal-stat/preference synchronization were implemented in Phase 2. External **RGSX catalog** integration remains planned for Phase 4.

The objective is to make the database the single source of truth.

---

## Plugin-Based Expansion

Support for new emulators should never require modifying Launcher PI itself.

Instead, new functionality will be added through plugins.

This architecture keeps the project scalable while making community contributions significantly easier.

---

## Cross-Platform Compatibility

Launcher PI has been designed from the beginning to support both Linux and Windows.

The game version system allows each operating system to use its own installation package while remaining under a single game entry.

---

## Organization

Every folder inside the project has a clearly defined responsibility.

Maintaining this organization keeps the codebase readable and allows the project to grow without becoming difficult to maintain.

---

# 🚀 Long-Term Vision

The ultimate goal of Launcher PI is to allow users to:

* Install games automatically
* Update games automatically
* Install emulators on demand
* Launch ROMs seamlessly
* Organize a unified game library
* Track play time
* Manage favorites
* Configure plugins
* Browse complete game information

—all without requiring manual configuration.

The launcher should be capable of handling everything behind the scenes, providing a smooth and beginner-friendly experience.

---

# 🤝 Contributing

Launcher PI is currently under active development.

Suggestions, bug reports and future contributions are always welcome.

As the architecture reaches stability, contribution guidelines and development documentation will also be published.

---

# 📄 License

The project's license will be defined before the first stable public release.

Until then, Launcher PI remains under active development.

---

# ❤️ Acknowledgements

Special thanks to everyone following and supporting the development of Launcher PI.

Every completed milestone brings the project one step closer to its primary goal:

Creating a unified platform capable of managing games from multiple platforms and technologies through a single modern application.

---

<div align="center">

# 🚀 Launcher PI

### A modern, modular and fully database-driven game launcher.

**Built with Python • CustomTkinter • SQLite**

---

⭐ **Actively developed**

Last updated: **October 20, 2026**

</div>
