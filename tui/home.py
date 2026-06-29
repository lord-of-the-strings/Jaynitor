"""Creates the dashboard in Textual"""

import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Checkbox, ProgressBar, Label
from textual.containers import Vertical, Horizontal
from utils.storage import calculate


class JaynitorTUI(App):
    """Class that defines the TUI app"""

    CSS = """
    Screen {
        background: #1a1b26;
        color: #a9b1d6;
    }
    Header {
        background: #1f2335;
        color: #7aa2f7;
        text-style: bold;
    }
    Footer {
        background: #1f2335;
        color: #7aa2f7;
    }
    #main_layout {
        padding: 1 2;
    }
    .panel-container {
        margin-bottom: 1;
        height: auto;
    }
    .panel-row {
        height: 1;
    }
    .panel-title {
        color: #7aa2f7;
        text-style: bold;
    }
    .panel-body-text {
        color: #c0caf5;
        margin-left: 2;
    }
    ProgressBar {
        margin: 0 2;
        width: 60;
    }
    ProgressBar Bar{
        height: 1;
    }
    ProgressBar > Bar > .bar--bar {
        color: #7aa2f7;
    }
    ProgressBar > Bar > .bar--track {
        color: #414868;
    } 
    .source-row {
        height: 1;
    }
    .source-row Checkbox {
        width: 56;
        background: transparent;
        border: none;
    }
    .status-lbl {
        color: #e0af68; 
    }
    """

    BINDINGS = [
        ("▲/▼", "navigate", "Navigate"),
        ("space", "toggle", "Toggle Target"),
        ("a", "toggle_all", "Toggle All"),
        ("s", "scan", "Start Scan"),
        ("tab", "switch", "Switch Panel"),
        ("?", "help", "Help"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Textual compose function with widgets"""
        yield Header(show_clock=False)

        with Vertical(id="main_layout"):
            #  Storage Overview Component Structure
            with Vertical(classes="panel-container"):
                yield Label(
                    "┌─ Storage Overview ────────────────────────────────────────────────────┐",
                    classes="panel-title",
                )
                yield Label(
                    "Total: -- GB │ Used: -- GB (-- %) │ Free: -- GB",
                    classes="panel-body-text",
                    id="storage_lbl",
                )
                yield ProgressBar(total=100, show_percentage=False, show_eta=False)
                yield Label(
                    "└───────────────────────────────────────────────────────────────────────┘",
                    classes="panel-title",
                )

            #  Cleanable Sources Checkbox List Structure
            with Vertical(classes="panel-container"):
                yield Label(
                    "┌─ Cleanable Sources ───────────────────────────────────────────────────┐",
                    classes="panel-title",
                )
                with Horizontal(classes="source-row"):
                    yield Checkbox("Pacman Cache (/var/cache/pacman/pkg)", value=False)
                    yield Label("[Pending Scan]", classes="status-lbl")

                with Horizontal(classes="source-row"):
                    yield Checkbox("Unused Orphan Packages (pacman -Qtdq)", value=False)
                    yield Label("[Pending Scan]", classes="status-lbl")

                with Horizontal(classes="source-row"):
                    yield Checkbox("User Cache (~/.cache)", value=False)
                    yield Label("[Pending Scan]", classes="status-lbl")

                with Horizontal(classes="source-row"):
                    yield Checkbox(
                        "Systemd Journal Logs (/var/log/journal)", value=False
                    )
                    yield Label("[Pending Scan]", classes="status-lbl")

                with Horizontal(classes="source-row"):
                    yield Checkbox("Broken Symlinks", value=False)
                    yield Label("[Pending Scan]", classes="status-lbl")

                yield Label(
                    "└───────────────────────────────────────────────────────────────────────┘",
                    classes="panel-title",
                )

        yield Footer()

    def on_mount(self) -> None:
        """Textual on_mount function with initial processes"""
        self.title = "Jaynitor v0.1 [Target: /]"
        self.sub_title = "[Host: archlinux]"
        self.run_worker(self.fetch_storage(), exclusive=True)

    async def fetch_storage(self) -> None:
        """Function to fetch storage info"""
        loop = asyncio.get_running_loop()
        data = await loop.run_in_executor(None, calculate)
        self.query_one(ProgressBar).progress = data["percentage"]
        self.query_one("#storage_lbl").update(data["ui"])


if __name__ == "__main__":
    app = JaynitorTUI()
    app.run()
