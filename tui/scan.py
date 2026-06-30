"""Secondary screen for scanning"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container
from textual.widgets import Header, Footer, Label


class DetailScreen(Screen):
    """Pacman cache view screen"""

    BINDINGS = [("escape", "app.pop_screen", "Back to Main")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("Welcome to the Secondary Screen!", id="screen-title"),
            Label("Press ESC to go back to the package list.", id="screen-desc"),
        )
        yield Footer()
