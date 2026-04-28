# app/ui/layouts.py
"""Layouts base para todas las pantallas."""

import tkinter as tk
from . import styles as s
from .components import BackBtn, Divider, StatusBar


class BaseScreen:
    """
    Pantalla base.  Todas las pantallas heredan de esta.

    Estructura:
      ┌──────────────────────────────┐
      │  top_bar  (back + título)    │
      │  divider                     │
      │  body  (fill/expand)         │
      │  status_bar                  │
      └──────────────────────────────┘
    """

    title = "Pantalla"

    def __init__(self, container, router):
        self.container = container
        self.router = router

    # ── plantilla pública ─────────────────────────────────────────────────────
    def render(self):
        """Construye la estructura fija y llama a build_body()."""
        self._build_shell()
        self.build_body(self.body)

    # ── estructura fija ───────────────────────────────────────────────────────
    def _build_shell(self):
        # Top bar
        self.top_bar = tk.Frame(self.container, bg=s.C_BG, pady=8)
        self.top_bar.pack(fill="x", padx=s.PAD_LG)

        self._add_back_button()

        tk.Label(self.top_bar, text=self.title,
                 font=s.F_H1, bg=s.C_BG, fg=s.C_DARK).pack(side="left", padx=12)

        # Acciones adicionales a la derecha
        self.toolbar = tk.Frame(self.top_bar, bg=s.C_BG)
        self.toolbar.pack(side="right")

        Divider(self.container).pack(fill="x")

        # Cuerpo principal
        self.body = tk.Frame(self.container, bg=s.C_BG)
        self.body.pack(fill="both", expand=True)

        # Barra de estado
        self.status = StatusBar(self.container)
        self.status.pack(fill="x", side="bottom")

    def _add_back_button(self):
        from ..modules.menu import MenuScreen
        BackBtn(self.top_bar,
                command=lambda: self.router.navigate(MenuScreen)).pack(side="left")

    # ── para sobreescribir ────────────────────────────────────────────────────
    def build_body(self, parent):
        raise NotImplementedError
