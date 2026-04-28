# app/modules/menu.py
"""Pantalla principal — menú de opciones."""

import tkinter as tk
from app.ui import styles as s
from app.ui.components import Divider


class MenuScreen:
    """Menú principal. No hereda BaseScreen para tener diseño propio."""

    ITEMS = [
        ("1", "UNIR SHEETS",        "Procesamiento múltiple por archivo",  "union_sheets"),
        ("2", "UNIR ARCHIVOS",       "Consolidación total de archivos",     "merge_files"),
        ("3", "SEPARAR SHEETS",      "Divide un Excel en archivos por hoja","split_sheets"),
        ("4", "FILTRAR & ORDENAR",   "Filtra, ordena y elige columnas",     "filter_module"),
        ("5", "NORMALIZAR DATOS",    "Detecta y unifica valores similares", "normalizer"),
    ]

    def __init__(self, container, router):
        self.container = container
        self.router    = router

    def render(self):
        # ── Header marca ─────────────────────────────────────────────────────
        header = tk.Frame(self.container, bg=s.C_DARK, pady=28)
        header.pack(fill="x")

        inner = tk.Frame(header, bg=s.C_DARK)
        inner.pack()

        tk.Label(inner, text="esan", font=s.F_BRAND,
                 bg=s.C_DARK, fg=s.C_RED).pack(side="left")
        tk.Label(inner, text=" | MEDICIONES", font=s.F_SUBBRAND,
                 bg=s.C_DARK, fg=s.C_GRAY_LT).pack(side="left", padx=10)

        # ── Subtítulo ─────────────────────────────────────────────────────────
        tk.Label(self.container,
                 text="Selecciona una herramienta para comenzar",
                 font=s.F_BODY, bg=s.C_BG, fg=s.C_GRAY_LT).pack(pady=(20, 4))

        Divider(self.container).pack(fill="x", padx=40, pady=4)

        # ── Grid de tarjetas ─────────────────────────────────────────────────
        grid = tk.Frame(self.container, bg=s.C_BG)
        grid.pack(expand=True, pady=20, padx=60)

        for i, (num, title, desc, route) in enumerate(self.ITEMS):
            r, c = divmod(i, 2)
            self._make_card(grid, num, title, desc, route).grid(
                row=r, column=c, padx=14, pady=14, sticky="nsew")

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        # ── Pie ───────────────────────────────────────────────────────────────
        tk.Label(self.container, text=f"FastEditable v2.0",
                 font=s.F_SMALL, bg=s.C_BG, fg=s.C_BORDER).pack(side="bottom", pady=10)

    # ── helpers ───────────────────────────────────────────────────────────────
    def _make_card(self, parent, num, title, desc, route):
        """Crea una tarjeta clickeable como botón invisible con contenido personalizado."""
        # Usar Button como contenedor (invisible, sin bordes)
        btn = tk.Button(
            parent,
            bg=s.C_BG_CARD,
            activebackground=s.C_BG_CARD,
            bd=0,
            relief="flat",
            cursor="hand2",
            width=42,
            height=7,
            command=lambda r=route: self._navigate(r)
        )
        
        # Crear un frame dentro del botón para el contenido
        content_frame = tk.Frame(btn, bg=s.C_BG_CARD,
                                highlightbackground=s.C_BORDER,
                                highlightthickness=1)
        content_frame.place(relwidth=1, relheight=1, x=0, y=0)
        btn.config(highlightthickness=0)

        num_lbl = tk.Label(content_frame, text=num, font=("Georgia", 28, "bold"),
                           bg=s.C_BG_CARD, fg=s.C_RED, cursor="hand2")
        num_lbl.pack(anchor="w", padx=28, pady=(22, 0))

        title_lbl = tk.Label(content_frame, text=title, font=s.F_H2,
                            bg=s.C_BG_CARD, fg=s.C_DARK, cursor="hand2")
        title_lbl.pack(anchor="w", padx=28, pady=(2, 4))

        desc_lbl = tk.Label(content_frame, text=desc, font=s.F_SMALL,
                           bg=s.C_BG_CARD, fg=s.C_GRAY_LT, wraplength=280,
                           justify="left", cursor="hand2")
        desc_lbl.pack(anchor="w", padx=28)

        # Flecha decorativa
        arrow_lbl = tk.Label(content_frame, text="→", font=("Segoe UI", 16),
                            bg=s.C_BG_CARD, fg=s.C_BORDER, cursor="hand2")
        arrow_lbl.pack(anchor="e", padx=28, pady=(8, 0))

        # Hover effects
        def on_enter(e):
            content_frame.config(highlightbackground=s.C_RED, highlightthickness=2)
            num_lbl.config(fg=s.C_RED_DK)

        def on_leave(e):
            content_frame.config(highlightbackground=s.C_BORDER, highlightthickness=1)
            num_lbl.config(fg=s.C_RED)

        # Bind hover y click en todos los widgets internos
        for widget in [content_frame, num_lbl, title_lbl, desc_lbl, arrow_lbl]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", lambda e, r=route: self._navigate(r))

        return btn

    def _navigate(self, route):
        from . import union_sheets, merge_files, split_sheets, filter_module, normalizer
        MAP = {
            "union_sheets":  union_sheets.UnionSheetsScreen,
            "merge_files":   merge_files.MergeFilesScreen,
            "split_sheets":  split_sheets.SplitSheetsScreen,
            "filter_module": filter_module.FilterScreen,
            "normalizer":    normalizer.NormalizerScreen,
        }
        if route in MAP:
            self.router.navigate(MAP[route])
