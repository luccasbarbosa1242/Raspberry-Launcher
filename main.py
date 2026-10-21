"""Composition root: the only module binding concrete frontend and backend."""

from application.controller import LauncherController
from backend.api import LauncherService
from backend.path_resolver import PathResolver
from contracts.models import UiResources


def main():
    # Lazy GUI import lets the backend run on systems without Tk or a display.
    from frontend.window import LauncherWindow

    backend = LauncherService()
    backend.initialize()
    controller = LauncherController(backend)
    window = LauncherWindow(controller, UiResources(
        str(PathResolver.assets() / "icons"),
        theme=backend.profile_settings().theme,
    ))
    controller.attach_view(window)
    window.start_polling(controller.poll)
    controller.navigate("home")
    try:
        window.run()
    finally:
        controller.close()


if __name__ == "__main__":
    main()
