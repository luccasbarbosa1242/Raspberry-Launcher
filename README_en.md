# Raspberry Launcher

Python desktop game launcher with separate presentation and backend code.

## Run

Python 3.10+ with Tk support is required.

```bash
python -m pip install -r requirements.txt
python main.py
```

## Layers

| Path | Responsibility |
| --- | --- |
| `frontend/` | CustomTkinter windows, screen layouts, visual styles and widget state. |
| `backend/` | Library, persistence, assets, downloads, installation, launching, scores and emulators. |
| `application/` | Controller, background tasks, navigation and main-thread delivery of results. |
| `contracts/` | Immutable data objects and protocols shared across the boundaries. |
| `main.py` | Composition root binding the concrete implementations. |

The frontend does not import the backend. The backend does not import the frontend or GUI libraries. The controller depends only on contracts, not on either concrete implementation. Both run in the same desktop process; no HTTP server is required.

## Independent frontend preview

```bash
python -m pip install -r requirements/frontend.txt
python -m frontend.preview
```

This preview renders fixture data and performs no real game operations.

## Independent backend

```bash
python -m pip install -r requirements/backend.txt
python -m backend --help
python -m backend list
python -m backend list --collection search --term Snake
python -m backend show snake
python -m backend.tools.health_check
```

Administrative tools previously under `tools/` now run as `python -m backend.tools.NAME`. Set `RASPBERRY_LAUNCHER_HOME` or use the backend CLI's `--home` option to isolate runtime data.

## Validation

```bash
python -m unittest discover -s tests -v
```

Graphical tests require a display or Xvfb. Tests use temporary databases and installation folders. The original `DATA`, `USERDATA` and `ASSETS` files remain intact in this archive.

Detailed Portuguese documentation: [architecture](docs/ARQUITETURA.md), [analysis and changes](docs/ANALISE_E_MUDANCAS.md), [validation](docs/VALIDACAO.md). The previous READMEs and full dependency list are retained in `docs/historico/` for reference.
