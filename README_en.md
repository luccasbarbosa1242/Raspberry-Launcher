<div align="center">

# 🚀 Launcher PI

🌎 Language:

* 🇺🇸 English (Current)
* 🇧🇷 [Versão em Português](README.md)

### Game Launcher built with Python, CustomTkinter and SQLite

Centralize native games, web games and ROMs into a single library.

### 📈 Development Status

> **Phase 1 Completed • Phase 2 In Progress (Steps 1–11 Completed) • UI and Application Logic Separated**

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

**Launcher PI** is a game launcher built with **Python**, using **CustomTkinter** for the graphical interface and **SQLite** as its primary database.

The project aims to centralize different types of games into a single library, allowing users to install, organize and launch their games through a modern and intuitive interface.

Launcher PI currently supports:

* 🎮 Native Games
* 🌐 Web Games
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
> ## 🔴 DATABASE MIGRATION IN PROGRESS
>
> Launcher PI is currently undergoing **Phase 2**, migrating to a fully database-driven architecture.
>
> During this phase, almost every system inside the launcher is being converted to rely exclusively on SQLite.
>
> The `games.py` file is still available only for temporary backward compatibility and will be removed in a future update.
>
> Database migrations now preserve existing data, meaning the database no longer needs to be recreated during development.

---

# 🎯 Current Priorities

> This section reflects the current focus of development.

---

# 🔴 Highest Priority

## Database (93%)

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
* [ ] Platform management through the database
* [ ] Emulator management through the database
* [ ] Complete removal of `games.py`

---

## Game System (92%)

* [x] Native games
* [x] Web games
* [x] Dynamic library
* [x] Automatic downloads
* [x] Automatic installation
* [x] Automatic uninstallation
* [x] Database-driven updates
* [x] Administrative registration tools
* [x] Multi-platform game versions (Linux / Windows)
* [x] Individual game pages

---

## Emulators (65%)

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

## Built-in Browser

* [ ] Fix current issues
* [ ] Improve launcher integration
* [ ] Better tab management

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

* [ ] Light theme
* [ ] Dark theme
* [ ] Background music
* [ ] Volume control
* [ ] Brightness control

---

## Users

* [ ] User profiles
* [ ] Individual statistics
* [ ] Gameplay history
* [ ] Configuration backup

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
* [ ] Cross-device synchronization
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

## 🌐 Web Games

* Opens games in the system default browser
* Direct launcher integration
* Fully database-driven registration

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

# 🆕 Latest Update — Separate UI and Application Logic

> **Restructuring completed • Downloads fixed • Uninstall menu restored**

## ✅ Delivered in This Update

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

---

## 📂 Layer Responsibilities

| Folder / File | Responsibility |
| --------------- | ----------------------- |
| `frontend/` | Windows, screens, cards, styles, rendered images and widget state |
| `backend/` | Application rules, SQLite, downloads, installation, uninstallation, launching and emulators |
| `application/` | Action coordination, navigation, background tasks and UI updates |
| `contracts/` | Shared data and public interfaces used by the layers |
| `main.py` | Application startup and wiring of concrete implementations |
| `backend/tools/` | Administrative command-line tools |
| `ASSETS/`, `DATA/`, `USERDATA/` | Project resources and data |

The interface sends actions containing identifiers and receives data ready for display. Widgets are never passed to the backend, and screens do not run SQL queries, downloads or installations.

---

## 🛠️ Included Fixes

* [x] Download calls compatible with `gdown 6.1.0`, removing the unsupported `fuzzy` argument
* [x] Asset downloads and game installation using the corrected download call
* [x] **Uninstall** action restored in the three-dot menu for installed non-web games
* [x] Uninstall availability fixed for local games and ROMs, including those outside the managed installation folder
* [x] Managed installation removal and record updates without deleting external executables or ROM files

---

## ▶️ Running Each Layer

Complete application:

```bash
python -m pip install -r requirements.txt
python main.py
```

UI preview using demonstration data:

```bash
python -m pip install -r requirements/frontend.txt
python -m frontend.preview
```

Backend from the terminal:

```bash
python -m pip install -r requirements/backend.txt
python -m backend --help
python -m backend list
```

Administrative tools now run as modules, for example: `python -m backend.tools.add_game`.

---

## 🧪 Update Validation

* [x] **43 automated tests passed** on Linux, including graphical tests with real CustomTkinter widgets on a virtual display
* [x] Python module compilation and static checks passed
* [x] **27 data and resource files preserved**, compared byte for byte with the original ZIP

Download tests used local files and controlled HTTP transport. The availability of every external catalog link was not validated, and tests were not run on Windows or with a real ROM in PCSX2.

Details: [Architecture](docs/ARQUITETURA.md), [Analysis and changes](docs/ANALISE_E_MUDANCAS.md) and [Validation](docs/VALIDACAO.md). These detailed documents are currently in Portuguese.

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

## Planned Database Tables

The following tables will complete the migration to a fully database-driven launcher:

```text
platforms
```

Stores every supported gaming platform.

---

```text
emulators
```

Stores every installed emulator.

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
* 🌐 Web Games
* 🕹️ ROMs
* ⚙️ Emulators
* 🖼️ Game Assets
* 📚 Unified Game Library

—all from a single application.

The long-term vision is to make Launcher PI entirely database-driven, allowing new games to be added without modifying the application's source code.

---

# 🗺️ Development Roadmap

## ✅ Phase 1 — Core Architecture (Completed)

The first development phase focused on building the technical foundation of Launcher PI.

Main achievements:

* Modular architecture
* Dynamic game library
* Download system
* Automatic installation
* Automatic uninstallation
* LauncherFactory
* NativeLauncher
* RomLauncher
* EmulatorManager
* Plugin system
* Asset system
* SQLite integration
* Initial user interface

This phase established the foundation for every future feature.

---

## 🚧 Phase 2 — Database Migration

The current phase focuses on migrating the entire launcher to a fully database-driven architecture.

Current objectives:

* Make SQLite the single source of truth.
* Remove every dependency on `games.py`.
* Register games using administrative tools.
* Register assets through the database.
* Support multiple platform-specific versions.
* Preserve user data through migrations.
* Prepare platforms and emulators for full database integration.

Delivered in this update:

* [x] Separate frontend, backend, application and contracts layers
* [x] Backend CLI and independent UI preview
* [x] Separate dependencies and preserved administrative tools
* [x] Google Drive download compatibility fix
* [x] Restored three-dot uninstall menu
* [x] 43 automated tests passed on Linux

Once completed, nearly every aspect of Launcher PI will be configurable through the database alone.

---

## ⏳ Phase 3 — Content Expansion

After the migration is complete, development will focus on expanding the launcher's ecosystem.

Planned additions include:

* More games
* More emulators
* More gaming platforms
* Collections
* Individual game pages
* Improved user interface
* Additional administrative tools

---

## 🚀 Phase 4 — Public Release

The final development phase will focus on preparing Launcher PI for public distribution.

Planned deliverables:

* Official installer
* Automatic updater
* Linux packages
* Windows packages
* Complete documentation
* Stable public release

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

Future versions will also manage:

* Platforms
* Emulators
* Collections
* User data

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
