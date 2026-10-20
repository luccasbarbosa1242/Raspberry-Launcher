"""Transient widget state; no installation rules, database or workers."""

from contracts.models import Phase

PHASE_TEXT = {
    Phase.STARTED: "Aguarde...",
    Phase.DOWNLOADING: "Baixando...",
    Phase.EXTRACTING: "Instalando...",
    Phase.REGISTERING: "Finalizando...",
}
KIND_TEXT = {"uninstall": "Removendo...", "launch": "Abrindo...", "favorite": "Salvando..."}


class WidgetBindings:
    def __init__(self):
        self.clear()

    def clear(self):
        self.buttons = {}
        self.scores = {}

    def button(self, key, widget, activity=False):
        self.buttons.setdefault(key, []).append(
            (widget, widget.cget("text"), widget.cget("state"), activity)
        )
        return widget

    def score(self, game_id, widget):
        self.scores.setdefault(game_id, []).append(widget)

    def set_operation(self, status):
        finished = status.phase in (Phase.COMPLETE, Phase.FAILED)
        for widget, text, state, activity in self.buttons.get(status.key, ()):
            if widget.winfo_exists():
                label = text
                if activity and not finished:
                    label = KIND_TEXT.get(status.kind, PHASE_TEXT.get(status.phase, "Aguarde..."))
                widget.configure(text=label, state=state if finished else "disabled")

    def set_scores(self, scores):
        for game_id, value in scores.items():
            for label in self.scores.get(game_id, ()):
                if label.winfo_exists():
                    label.configure(text=f"Best Score: {value}")
