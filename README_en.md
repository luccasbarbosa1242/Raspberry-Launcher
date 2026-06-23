<div align="center">

# 🚀 Launcher PI

🌎 Language:

- 🇺🇸 English (Current)
- 🇧🇷 [Versão em Português](README.md)

### Game Launcher built with Python, CustomTkinter and SQLite

Centralize native games, web games and ROMs into a single library.

### 📈 Overall Development Progress

████████░░  81%

<img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/CustomTkinter-UI-green?style=for-the-badge" />
<img src="https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/Status-In%20Development-orange?style=for-the-badge" />

</div>

---

# 📖 About the Project

Launcher PI is a game launcher developed in Python with a focus on simplicity, organization, and automation.

The goal of the project is to allow users to manage:

- 🎮 Native Games
- 🌐 Web Games
- 🕹️ ROMs
- ⚙️ Emulators

All through a single interface.

In addition, the launcher is being developed to automatically handle downloads, installations, and configurations, minimizing the need for manual user intervention.

---

# ⚠️ Important Notice

> [!CAUTION]
>
> ## 🔴 DATABASE TRANSITION IN PROGRESS
>
> The project is currently in Phase 2 of its migration to a fully SQLite-based system.
>
> The goal is to completely remove the dependency on the `games.py` file, making the database the launcher's only source of data.
>
> During this phase, manual modifications to the database are not recommended.

---

# 🎯 Current Priorities

> This section represents the current development focus.

## 🔴 Highest Priority

### Database (85%)

- [x] SQLite structure created
- [x] Repositories implemented
- [x] Library integrated with the database
- [x] Asset system integrated
- [x] Installation persistence
- [ ] Migrations without deleting the database
- [ ] Complete removal of `games.py`
- [ ] Database administration tools

### Emulators (60%)

- [x] Core structure created
- [x] EmulatorManager
- [x] PackageResolver
- [x] PluginLoader
- [x] PluginRegistry
- [x] RomLauncher
- [ ] Real emulator downloads
- [ ] Fully automated installation
- [ ] Final ROM integration
- [ ] Emulator library

### Game System (80%)

- [x] Native games
- [x] Web games
- [x] Automatic installation
- [x] Automatic uninstallation
- [x] Database-integrated library
- [ ] 100% database-driven game registration
- [ ] Game update system

---

## 🟠 High Priority

### Interface (75%)

- [x] Functional library
- [x] Card system
- [x] Covers through AssetManager
- [x] Visual game status indicators
- [x] Database-integrated Home page
- [ ] Individual game page
- [ ] Final visual improvements
- [ ] Animations and visual feedback

### Internal Browser

- [ ] Fix current issues
- [ ] Improve launcher integration

---

## 🟡 Medium Priority

### Library

- [ ] Individual game page
- [ ] Game descriptions
- [ ] Genres
- [ ] Release year
- [ ] Emulator information

### Content

- [ ] Add more games
- [ ] Add more emulators

---

## 🟢 Low Priority

### Settings

- [ ] Light/Dark theme
- [ ] Background music
- [ ] Volume control
- [ ] Brightness control

### Users

- [ ] User profiles
- [ ] Individual statistics

### Distribution

- [ ] Fix external executables
- [ ] Create an official Launcher PI installer

---

## 🔵 Future Ideas

- [ ] Achievement system
- [ ] Cloud backups
- [ ] Device synchronization
- [ ] Theme store

# ✨ Features

## 🎮 Native Games

- Automatic installation
- Automatic downloads
- Integrated execution
- Linux support
- Windows support

## 🌐 Web Games

- Internal browser
- Direct launcher integration

## 🕹️ ROMs and Emulators

- Structure prepared for ROM integration
- Emulator plugin system
- Automatic emulator downloads (in development)

## 📊 Library

- Centralized library
- Score system
- Installed game management

## 🖼️ Assets

- AssetManager
- AssetRepository
- Local cache
- Remote covers
- Fallback system

---

# 🏗️ Project Architecture

```text
launcher-pi/

CORE/
├── assets/
├── database/
├── download/
├── emulators/
├── launchers/
├── library/
├── plugins/

DATA/
├── library.db
├── emulator_packages.json

DOWNLOADS/
EMULATORS/
USERDATA/

UI/
├── views/
├── cards.py
├── pages.py
├── window.py

UTILS/
tools/

main.py
```
## CORE/database

Responsible for:

- SQLite
- Migrations
- Data persistence

## CORE/library

Responsible for:

- Game library
- Repositories
- Data management and queries

## CORE/launchers

Responsible for:

- NativeLauncher
- RomLauncher
- LauncherFactory

## CORE/emulators

Responsible for:

- Emulator downloads
- Automatic installation
- Version management

## CORE/plugins

Responsible for:

- Plugin registration
- Emulator adapters
- System extensibility

---

# 🔄 System Flow

```text
User
    │
    ▼
Library
    │
    ▼
LauncherFactory
    │
    ├──────────────► NativeLauncher
    │                    │
    │                    ▼
    │                Executable
    │
    └──────────────► RomLauncher
                         │
                         ▼
                   EmulatorManager
                         │
                         ▼
                        ROM
```

---

# 🛠️ Technologies Used

| Technology | Usage |
|------------|------------|
| Python | Backend |
| CustomTkinter | Interface |
| SQLite3 | Database |
| Git | Version Control |
| GitHub Releases | Distribution |
| Google Drive | Temporary Distribution |

---

# 📊 Current Status

| Area | Progress |
|--------|--------|
| Launcher Core | ✅ 100% |
| Library | ✅ 85% |
| Database | 🚧 85% |
| Assets | 🚧 80% |
| Downloads | ✅ 90% |
| Web Games | ✅ 90% |
| Native Games | ✅ 85% |
| Emulators | 🚧 60% |
| Plugins | 🚧 65% |
| Interface | 🚧 75% |

---

# 🚀 Overall Progress

```text
Launcher Core         ██████████ 100%
Library               ████████░░  85%
Database              ████████░░  85%
Assets                ████████░░  80%
Downloads             █████████░  90%
Native Games          ████████░░  85%
Web Games             █████████░  90%
Emulators             ██████░░░░  60%
Plugins               ██████░░░░  65%
Interface             ███████░░░  75%
```

---

# 📋 Roadmap

## ✅ Completed

### Architecture

- [x] Complete project modularization
- [x] LauncherFactory
- [x] NativeLauncher
- [x] RomLauncher
- [x] EmulatorManager
- [x] Plugin system
- [x] SQLite integration

### Library

- [x] SQLite-based library
- [x] Dynamic cards
- [x] Remote covers
- [x] Asset cache
- [x] Visual game status system

### Installation

- [x] Automatic downloads
- [x] Automatic installation
- [x] Automatic uninstallation
- [x] Database persistence

---

## 🚧 In Development

### Database - Phase 2

- [ ] Database migrations without deletion
- [ ] Tool-based game registration
- [ ] Tool-based asset registration
- [ ] Removal of `games.py` dependency

### Emulators

- [ ] Real downloads
- [ ] Real installation
- [ ] Full ROM integration

### Interface

- [ ] Individual game pages
- [ ] Detailed information
- [ ] Screenshots
- [ ] Visual improvements

---

## ⏳ Planned

### 👤 Users

- [ ] User profiles
- [ ] Individual statistics

### 🎮 Library

- [ ] Individual game pages
- [ ] Game descriptions
- [ ] Genres
- [ ] Release year
- [ ] Emulator information

### 📦 Installation

- [ ] Silent installers
- [ ] Manual game addition
- [ ] Manual installer addition
- [ ] Manual emulator addition

### ⚙️ Settings

- [ ] Light/Dark theme
- [ ] Background music
- [ ] Volume control
- [ ] Brightness control
- [ ] Advanced settings

### 🕹️ Content

- [ ] Add new games
- [ ] Add new emulators

### 📦 Distribution

- [ ] Fix external executables
- [ ] Create an official Launcher PI installer

### 🌐 Browser

- [ ] Improve integration
- [ ] Fix current issues

---

# 🎯 Final Goal

The goal of Launcher PI is to become a unified platform for game management, allowing users to access:

- Native Games
- Web Games
- ROMs
- Emulators

Through a single modern, simple, and automated interface.

Launcher PI is now entering its second major development phase.

Phase 1 focused on building the project's core architecture:

- Database
- Library
- Downloads
- Installation
- Assets
- Emulator system
- Plugin system

### ✅ Phase 1 Completed

Main achievements:

- SQLite integration
- LibraryManager
- GameRepository
- AssetManager
- AssetRepository
- NativeLauncher
- RomLauncher
- LauncherFactory
- EmulatorManager
- PluginLoader
- PluginRegistry
- Automatic game installation
- Automatic game uninstallation
- Internal browser integration
- Dynamic cards
- Remote asset support
- Cover cache system
- Visual game status system

### 🚧 Phase 2 In Progress

Current focus:

- Remove dependency on `games.py`
- Make SQLite the single source of truth
- Database migration system
- Administrative tools
- Game registration tools
- Asset registration tools
- Emulator registration tools
- ROM registration tools
- Individual game pages
- Full ROM + Emulator integration

The long-term goal is to allow games, ROMs, emulators, covers, banners and metadata to be managed entirely through the database, without requiring code changes.

---

# 🗺️ Development Phases

## Phase 1 — Core Architecture ✅

- [x] Database foundation
- [x] Library system
- [x] Download system
- [x] Installation system
- [x] Asset system
- [x] Launcher system
- [x] Emulator foundation
- [x] Plugin foundation

## Phase 2 — Database Driven Launcher 🚧

- [ ] Database migrations
- [ ] Administrative tools
- [ ] Game registration
- [ ] Asset registration
- [ ] Emulator registration
- [ ] ROM registration
- [ ] Full removal of `games.py`

## Phase 3 — Content & Experience ⏳

- [ ] Individual game pages
- [ ] Metadata system
- [ ] Screenshots
- [ ] Statistics
- [ ] Search and filters
- [ ] Collections

## Phase 4 — Distribution & Polish ⏳

- [ ] Official installer
- [ ] Linux packages
- [ ] Windows packages
- [ ] Automatic updates
- [ ] Final UI polish

---

# 🤝 Contributing

Contributions are welcome.

If you plan to contribute to database-related features, please check the current migration stage before modifying database structures.

During Phase 2, database architecture is considered highly sensitive and may change frequently.

---

# 📜 License

This project is currently under development.

License information will be defined before the first stable public release.

---

<div align="center">

### 🚀 Project Under Active Development

Phase 2 — Database Driven Launcher

Last Updated: June 2026

</div>