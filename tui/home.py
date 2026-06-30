"""Creates the dashboard in Textual"""

import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Checkbox, ProgressBar, Label
from textual.containers import Vertical, Horizontal
from tui.scan import DetailScreen
from utils.storage import calculate


class JaynitorTUI(App):
    """Class that defines the TUI app"""

    # Combined stylesheet supporting both explicit Tokyo Night and reactive System theme
    CSS = """
    /* --- Base Layout --- */
    #main_layout {
        padding: 1 2;
        height: 1fr;
    }
    
    .panel-container {
        margin-bottom: 1;
        height: auto;
        padding: 0 1;
        border: round; 
    }
    
    .panel-body-text {
        margin: 0 0 1 1;
    }
    
    ProgressBar {
        margin: 0 1 1 1;
        width: 100%;
    }
    
    ProgressBar Bar {
        height: 1;
    }
    
    .source-row {
        height: 1;
        margin-bottom: 0;
    }
    
    .source-row Checkbox {
        width: 45;
        background: transparent;
        border: none;
    }

    /* Tokyo Night */
    Screen.theme-tokyo {
        background: #1a1b26;
    }
    .theme-tokyo Header, .theme-tokyo Footer {
        background: #1f2335;
        color: #7aa2f7;
    }
    .theme-tokyo .panel-container {
        border: round #7aa2f7; /* Crisp blue panel borders */
    }
    .theme-tokyo .panel-body-text {
        color: #c0caf5;
    }
    .theme-tokyo ProgressBar > Bar > .bar--bar {
        color: #7aa2f7;
    }
    .theme-tokyo ProgressBar > Bar > .bar--track {
        color: #414868;
    } 
    .theme-tokyo .status-lbl {
        color: #e0af68; 
    }
    .theme-tokyo Checkbox {
        color: #a9b1d6;
    }

    /* System-Reactive (Obeys Pywal / Wallust / Hyprland Config)  */
    Screen.theme-system {
        background: transparent; /* Allows terminal blur and transparency to show through */
    }
    .theme-system Header, .theme-system Footer {
        background: transparent;
        color: $accent; /* Inherits terminal primary accent color token */
    }
    .theme-system .panel-container {
        border: round $accent; /* Uses system accent color */
    }
    .theme-system .panel-body-text, .theme-system Checkbox {
        color: $text; /* Inherits system text colors */
    }
    .theme-system ProgressBar > Bar > .bar--bar {
        color: $accent;
    }
    .theme-system ProgressBar > Bar > .bar--track {
        color: $surface; /* Uses standard container fill color token */
    } 
    .theme-system .status-lbl {
        color: $warning; /* Gracefully degrades to system theme warning color token */
    }
    """

    BINDINGS = [
        ("▲/▼", "navigate", "Navigate"),
        ("space", "toggle", "Toggle Target"),
        ("a", "toggle_all", "Toggle All"),
        ("s", "show_secondary", "Start Scan"),
        ("t", "toggle_theme", "Toggle Theme"),
        ("tab", "switch", "Switch Panel"),
        ("?", "help", "Help"),
        ("q", "quit", "Quit"),
    ]

    SCREENS = {"secondary": DetailScreen}

    def compose(self) -> ComposeResult:
        """Textual compose function with widgets"""
        yield Header(show_clock=False)

        with Vertical(id="main_layout"):
            with Vertical(classes="panel-container", id="storage-panel"):
                yield Label(
                    "Total: -- GB │ Used: -- GB (-- %) │ Free: -- GB",
                    classes="panel-body-text",
                    id="storage_lbl",
                )
                yield ProgressBar(total=100, show_percentage=False, show_eta=False)

            with Vertical(classes="panel-container", id="sources-panel"):
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

        yield Footer()

    def on_mount(self) -> None:
        """Textual on_mount function with initial processes"""
        self.title = "Jaynitor v0.1 [Target: /]"
        self.sub_title = "[Host: archlinux]"

        self.query_one("#storage-panel").border_title = "Storage Overview"
        self.query_one("#sources-panel").border_title = "Cleanable Sources"

        # Set default theme (True adds class, False removes class)
        self.screen.set_class(True, "theme-tokyo")
        self.screen.set_class(False, "theme-system")

        self.run_worker(self.fetch_storage(), exclusive=True)

    def action_toggle_theme(self) -> None:
        """Action mapped to 't' to dynamically flip theme states"""
        is_tokyo = self.screen.has_class("theme-tokyo")
        self.screen.set_class(not is_tokyo, "theme-tokyo")
        self.screen.set_class(is_tokyo, "theme-system")

    def action_show_secondary(self) -> None:
        """Action to push the secondary screen (mapped to 's)"""
        self.push_screen("secondary")

    async def fetch_storage(self) -> None:
        """Function to fetch storage info"""
        loop = asyncio.get_running_loop()
        data = await loop.run_in_executor(None, calculate)
        self.query_one(ProgressBar).progress = data["percentage"]
        self.query_one("#storage_lbl").update(data["ui"])


if __name__ == "__main__":
    app = JaynitorTUI()
    app.run()
