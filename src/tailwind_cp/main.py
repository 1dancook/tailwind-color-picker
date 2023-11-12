"""
A simple utility for picking a color.
The palette is copied from tailwindcss.
See tailwind docs: https://tailwindcss.com/docs/customizing-colors
"""

from dataclasses import dataclass
from pyperclip import copy
from textual.app import App
from textual.widgets import DataTable, Static, Header
from textual.containers import Container
from rich.text import Text


CELL_WIDTH = 3

COLUMNS = ["50","100","200","300","400","500","600","700","800","900","950"]

ROWS = [
    ("Slate", "#f8fafc", "#f1f5f9", "#e2e8f0", "#cbd5e1", "#94a3b8", "#64748b", "#475569", "#334155", "#1e293b", "#0f172a", "#020617"),
    ("Gray", "#f9fafb", "#f3f4f6", "#e5e7eb", "#d1d5db", "#9ca3af", "#6b7280", "#4b5563", "#374151", "#1f2937", "#111827", "#030712"),
    ("Zinc", "#fafafa", "#f4f4f5", "#e4e4e7", "#d4d4d8", "#a1a1aa", "#71717a", "#52525b", "#3f3f46", "#27272a", "#18181b", "#09090b"),
    ("Neutral", "#fafafa", "#f5f5f5", "#e5e5e5", "#d4d4d4", "#a3a3a3", "#737373", "#525252", "#404040", "#262626", "#171717", "#0a0a0a"),
    ("Stone", "#fafaf9", "#f5f5f4", "#e7e5e4", "#d6d3d1", "#a8a29e", "#78716c", "#57534e", "#44403c", "#292524", "#1c1917", "#0c0a09"),
    ("Red", "#fef2f2", "#fee2e2", "#fecaca", "#fca5a5", "#f87171", "#ef4444", "#dc2626", "#b91c1c", "#991b1b", "#7f1d1d", "#450a0a"),
    ("Orange", "#fff7ed", "#ffedd5", "#fed7aa", "#fdba74", "#fb923c", "#f97316", "#ea580c", "#c2410c", "#9a3412", "#7c2d12", "#431407"),
    ("Amber", "#fffbeb", "#fef3c7", "#fde68a", "#fcd34d", "#fbbf24", "#f59e0b", "#d97706", "#b45309", "#92400e", "#78350f", "#451a03"),
    ("Yellow", "#fefce8", "#fef9c3", "#fef08a", "#fde047", "#facc15", "#eab308", "#ca8a04", "#a16207", "#854d0e", "#713f12", "#422006"),
    ("Lime", "#f7fee7", "#ecfccb", "#d9f99d", "#bef264", "#a3e635", "#84cc16", "#65a30d", "#4d7c0f", "#3f6212", "#365314", "#1a2e05"),
    ("Green", "#f0fdf4", "#dcfce7", "#bbf7d0", "#86efac", "#4ade80", "#22c55e", "#16a34a", "#15803d", "#166534", "#14532d", "#052e16"),
    ("Emerald", "#ecfdf5", "#d1fae5", "#a7f3d0", "#6ee7b7", "#34d399", "#10b981", "#059669", "#047857", "#065f46", "#064e3b", "#022c22"),
    ("Teal", "#f0fdfa", "#ccfbf1", "#99f6e4", "#5eead4", "#2dd4bf", "#14b8a6", "#0d9488", "#0f766e", "#115e59", "#134e4a", "#042f2e"),
    ("Cyan", "#ecfeff", "#cffafe", "#a5f3fc", "#67e8f9", "#22d3ee", "#06b6d4", "#0891b2", "#0e7490", "#155e75", "#164e63", "#083344"),
    ("Sky", "#f0f9ff", "#e0f2fe", "#bae6fd", "#7dd3fc", "#38bdf8", "#0ea5e9", "#0284c7", "#0369a1", "#075985", "#0c4a6e", "#082f49"),
    ("Blue", "#eff6ff", "#dbeafe", "#bfdbfe", "#93c5fd", "#60a5fa", "#3b82f6", "#2563eb", "#1d4ed8", "#1e40af", "#1e3a8a", "#172554"),
    ("Indigo", "#eef2ff", "#e0e7ff", "#c7d2fe", "#a5b4fc", "#818cf8", "#6366f1", "#4f46e5", "#4338ca", "#3730a3", "#312e81", "#1e1b4b"),
    ("Violet", "#f5f3ff", "#ede9fe", "#ddd6fe", "#c4b5fd", "#a78bfa", "#8b5cf6", "#7c3aed", "#6d28d9", "#5b21b6", "#4c1d95", "#2e1065"),
    ("Purple", "#faf5ff", "#f3e8ff", "#e9d5ff", "#d8b4fe", "#c084fc", "#a855f7", "#9333ea", "#7e22ce", "#6b21a8", "#581c87", "#3b0764"),
    ("Fuchsia", "#fdf4ff", "#fae8ff", "#f5d0fe", "#f0abfc", "#e879f9", "#d946ef", "#c026d3", "#a21caf", "#86198f", "#701a75", "#4a044e"),
    ("Pink", "#fdf2f8", "#fce7f3", "#fbcfe8", "#f9a8d4", "#f472b6", "#ec4899", "#db2777", "#be185d", "#9d174d", "#831843", "#500724"),
    ("Rose", "#fff1f2", "#ffe4e6", "#fecdd3", "#fda4af", "#fb7185", "#f43f5e", "#e11d48", "#be123c", "#9f1239", "#881337", "#4c0519"),
    ]



@dataclass
class ColorCell:
    """
    A dataclass to hold the value of a color.

    As a rich renderable, it will display as a block
    using it's color for the background.
    """

    value: str # hex color starting with hash

    def __rich__(self):
        # A block of CELL_WIDTH spaces wide, using it's value as the background color
        return Text(" "*CELL_WIDTH, f"white on {self.value}")

    def __str__(self):
        return str(self.value)


def get_color_index(col: int) -> int:
    """ Return a complementary color index for the given index """
    
    if col < 4:
        return col + 6
    elif col < 8:
        return col - 6
    elif col >= 8:
        return col - 8
    return 0


class Palette(DataTable):
    """
    A datatable that holds a palette

    Cells are ColorCell objects

    When the cell is selected it is copied to the clipboard.
    """

    BINDINGS = [
            ("j", "cursor_down", "Down"),
            ("k", "cursor_up", "Up"),
            ("h", "cursor_left", "Left"),
            ("l", "cursor_right", "Right"),
            ("y", "select_cursor", "Yank"),
            ]

    def on_mount(self):
        self.add_columns(*[x.center(CELL_WIDTH) for x in COLUMNS])
        for row in ROWS:
            cells = [ColorCell(value) for value in row[1:]]
            self.add_row(*cells, label=row[0], key=row[0])

    def on_data_table_cell_selected(self, event):
        hex_code = str(event.value)
        copy(hex_code)
        self.notify(f"Yanked {hex_code}")

class TailWindPicker(App):
    """
    A Tailwind Color Picker

    Bindings:

        j / down   - move cursor down
        k / up     - move cursor up
        h / left   - move cursor left
        l / right  - move cursor right
        y / enter  - yank (copy) the select color
        q / Ctrl+c - quit

    Selecting a color with the mouse will copy it.
    """

    BINDINGS = [
            ("q", "quit", "Quit"),
            ("?", "help", "Help"),
            ]


    CSS = """
    Screen {
        background: #1e293b;
        }

    #grid {
        layout: grid;
        grid-size: 1 2;
        grid-gutter: 0;
        grid-rows: 25 1fr;
        margin: 1 0;
        }

    .grid-cell {
        align: center top;
        }

    Palette {
        background: #ffffff; 
        padding: 1; 
        width: 66;
        height: 25;
        }

    .datatable--cursor {
        background: red;
        }

    .datatable--header {
        background: white 0%;
        color: #475569;
        }

    #static-text {
        margin: 0 1; 
        padding: 2 1; 
        height: 7; 
        background: #ffffff; 
        text-align: center; 
        border: wide black;
        width: 66;
        }

    """

    def compose(self):
        yield Header()
        with Container(id="grid"):
            with Container(classes="grid-cell"):
                yield Palette()
            with Container(classes="grid-cell"):
                yield Static(id="static-text")

    def on_mount(self):
        self.title = "Tailwind Color Pickerator"

    def on_data_table_cell_highlighted(self, event):
        """
        Change the fg and bg of the static widget
        based on the highlighted datatable cell
        """

        hex_code = str(event.value)
        palette = event.control

        # get a color that works well for foreground text
        # given the currently selected color used
        # as background
        row, col = palette.cursor_coordinate
        row_cells = palette.get_row_at(row)
        text_color_index = get_color_index(col)
        text_color = str(row_cells[text_color_index])

        # Update the static widget style and text
        static = self.get_widget_by_id("static-text")
        static.styles.background = hex_code
        static.styles.color = text_color
        static.update(
                f"Hex Value: {hex_code}"
                )

def main():
    twp = TailWindPicker()
    twp.run()

if __name__ == "__main__":
    main()
