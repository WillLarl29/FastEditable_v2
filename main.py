"""FILTER — MEDICIONES  v2.0
Punto de entrada principal.
"""

import tkinter as tk
from app.core.config import APP_TITLE, APP_WIDTH, APP_HEIGHT
from app.core.router import Router
from app.ui import styles as s
from app.modules.menu import MenuScreen


class FastEditableApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.configure(bg=s.C_BG)
        self.root.minsize(860, 600)

        # Contenedor raíz para el router
        container = tk.Frame(self.root, bg=s.C_BG)
        container.pack(fill="both", expand=True)

        self.router = Router(container)
        self.router.navigate(MenuScreen)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    FastEditableApp().run()
