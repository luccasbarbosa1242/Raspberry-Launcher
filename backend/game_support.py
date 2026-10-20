"""Execution policy shared by catalog validation and launchers.

HTTP remains a valid download transport. Only an execution path pointing to a
browser game is unsupported.
"""

from pathlib import PurePath


BROWSER_TYPES = frozenset({"html", "html5", "web", "browser", "url"})


def _field(record, name, default=""):
    try:
        value = record[name]
    except (KeyError, IndexError, TypeError):
        return default
    return value if value is not None else default


def browser_game(record):
    """Accept plain mappings and sqlite.Row without depending on SQLite."""
    for name in ("type", "launch_type", "platform"):
        if str(_field(record, name)).strip().lower() in BROWSER_TYPES:
            return True
    path = str(_field(record, "path")).strip()
    return path.lower().startswith(("http://", "https://")) or PurePath(
        path.split("?", 1)[0].split("#", 1)[0].replace("\\", "/")
    ).suffix.lower() in {".htm", ".html", ".xhtml"}


def require_supported_game(record):
    """Prevent browser execution even for a caller bypassing catalog queries."""
    if _field(record, "archived", False) or browser_game(record):
        raise ValueError("Jogos HTML/de navegador não são suportados; o histórico foi preservado.")


def active_catalog_sql(alias="", *, version=False):
    """Filter legacy browser rows inserted outside the supported services too.

    The alias is supplied only by repository code, never from user input.
    """
    prefix = f"{alias}." if alias else ""
    names = ("launch_type", "platform") if version else ("type", "launch_type", "platform")
    fields = [f"lower(trim(coalesce({prefix}{name}, '')))" for name in names]
    path = f"lower(trim(coalesce({prefix}path, '')))"
    return " AND ".join(
        [f"{prefix}archived = 0"]
        + [f"{field} NOT IN ('html', 'html5', 'web', 'browser', 'url')" for field in fields]
        + [
            f"{path} NOT LIKE 'http://%'",
            f"{path} NOT LIKE 'https://%'",
            *[
                f"{path} NOT LIKE '{pattern}'"
                for suffix in ("htm", "html", "xhtml")
                for pattern in (f"%.{suffix}", f"%.{suffix}?%", f"%.{suffix}#%")
            ],
        ]
    )
