# app/modules/filter_module.py
"""
Módulo: Filtrar & Ordenar — rediseño completo.

Características:
  • Filtros inteligentes por tipo de dato:
      - texto/objeto  → checkboxes con valores únicos
      - numérico      → rango min/max + campo libre
      - fecha         → rango de fechas
  • Ordenamiento múltiple (drag para reordenar criterios)
  • Selección / deselección de columnas con arrastrar
  • Vista previa en vivo (primeras N filas)
  • Validación y mensajes de estado claros
"""

import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from app.ui import styles as s
from app.ui.components import (
    PrimaryBtn, SecondaryBtn, GhostBtn, IconBtn,
    Card, ScrollableFrame, Divider, Badge, BodyLabel,
)
from app.ui.layouts import BaseScreen


# ─────────────────────────────────────────────────────────────────────────────
#  Helpers de tipo
# ─────────────────────────────────────────────────────────────────────────────

def _col_kind(series: pd.Series) -> str:
    """Devuelve 'numeric', 'datetime', o 'text'."""
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    try:
        converted = pd.to_datetime(series, errors="coerce")
        if converted.notna().mean() > 0.7:
            return "datetime"
    except Exception:
        pass
    return "text"


# ─────────────────────────────────────────────────────────────────────────────
#  Panel de filtro por columna
# ─────────────────────────────────────────────────────────────────────────────

class ColumnFilterPanel(tk.Frame):
    """
    Panel colapsable para filtrar una columna.
    Muestra controles apropiados según el tipo de dato.
    """

    def __init__(self, parent, col: str, series: pd.Series, on_change, **kw):
        super().__init__(parent, bg=s.C_BG_CARD, **kw)
        self.col      = col
        self.series   = series
        self.kind     = _col_kind(series)
        self.on_change = on_change
        self._expanded = False

        # Estado del filtro
        self._check_vars: dict[str, tk.BooleanVar] = {}
        self._num_min    = tk.StringVar()
        self._num_max    = tk.StringVar()
        self._date_from  = tk.StringVar()
        self._date_to    = tk.StringVar()
        self._search_var = tk.StringVar()

        self._build()

    # ── construcción ─────────────────────────────────────────────────────────
    def _build(self):
        # Encabezado (siempre visible)
        hdr = tk.Frame(self, bg=s.C_BG_CARD, cursor="hand2")
        hdr.pack(fill="x", padx=4, pady=2)
        hdr.bind("<Button-1>", self._toggle)

        self._arrow = tk.Label(hdr, text="▶", font=s.F_SMALL,
                               bg=s.C_BG_CARD, fg=s.C_GRAY_LT, cursor="hand2")
        self._arrow.pack(side="left", padx=(4, 6))
        self._arrow.bind("<Button-1>", self._toggle)

        tk.Label(hdr, text=self.col, font=s.F_BODY,
                 bg=s.C_BG_CARD, fg=s.C_DARK).pack(side="left")

        kind_map = {"numeric": ("123", "info"), "datetime": ("📅", "warn"), "text": ("Aa", "neutral")}
        sym, kind = kind_map[self.kind]
        Badge(hdr, sym, kind=kind).pack(side="left", padx=6)

        self._active_badge = Badge(hdr, "activo", kind="red")
        # se mostrará solo cuando haya filtro

        Divider(self).pack(fill="x")

        # Contenido (colapsable)
        self._body = tk.Frame(self, bg=s.C_BG_CARD)

        if self.kind == "text":
            self._build_text_filter()
        elif self.kind == "numeric":
            self._build_numeric_filter()
        elif self.kind == "datetime":
            self._build_date_filter()

    def _build_text_filter(self):
        # Búsqueda rápida
        search_f = tk.Frame(self._body, bg=s.C_BG_CARD)
        search_f.pack(fill="x", padx=8, pady=(6, 2))
        tk.Label(search_f, text="Buscar:", font=s.F_SMALL,
                 bg=s.C_BG_CARD, fg=s.C_GRAY_LT).pack(side="left")
        search_e = tk.Entry(search_f, textvariable=self._search_var,
                            font=s.F_SMALL, bg=s.C_BG,
                            relief="flat", highlightbackground=s.C_BORDER,
                            highlightthickness=1)
        search_e.pack(side="left", fill="x", expand=True, padx=(4, 0))
        self._search_var.trace_add("write", lambda *_: self._refresh_checkboxes())

        # Botones seleccionar/deseleccionar
        btn_row = tk.Frame(self._body, bg=s.C_BG_CARD)
        btn_row.pack(fill="x", padx=8, pady=2)
        GhostBtn(btn_row, "✓ Todo", command=self._select_all).pack(side="left")
        GhostBtn(btn_row, "✗ Nada", command=self._deselect_all).pack(side="left", padx=4)

        # Área de checkboxes
        self._cb_scroll = ScrollableFrame(self._body, bg=s.C_BG_CARD)
        self._cb_scroll.pack(fill="x", padx=8, pady=(2, 6))
        self._cb_scroll.canvas.config(height=120)
        self._refresh_checkboxes()

    def _build_numeric_filter(self):
        row = tk.Frame(self._body, bg=s.C_BG_CARD)
        row.pack(fill="x", padx=8, pady=6)

        def _entry(parent, var, label):
            tk.Label(parent, text=label, font=s.F_SMALL,
                     bg=s.C_BG_CARD, fg=s.C_GRAY_LT).pack(side="left")
            e = tk.Entry(parent, textvariable=var, width=10, font=s.F_BODY,
                         bg=s.C_BG, relief="flat",
                         highlightbackground=s.C_BORDER, highlightthickness=1)
            e.pack(side="left", padx=(2, 10))
            return e

        _entry(row, self._num_min, "Mínimo:")
        _entry(row, self._num_max, "Máximo:")

        # Estadísticas rápidas
        vmin = self.series.min()
        vmax = self.series.max()
        vmean = self.series.mean()
        stats = f"min={vmin:.2g}  max={vmax:.2g}  media={vmean:.2g}"
        tk.Label(self._body, text=stats, font=s.F_MONO,
                 bg=s.C_BG_CARD, fg=s.C_GRAY_LT).pack(padx=8, anchor="w", pady=(0, 6))

        self._num_min.trace_add("write", lambda *_: self.on_change())
        self._num_max.trace_add("write", lambda *_: self.on_change())

    def _build_date_filter(self):
        row = tk.Frame(self._body, bg=s.C_BG_CARD)
        row.pack(fill="x", padx=8, pady=6)

        for var, lbl in [(self._date_from, "Desde (YYYY-MM-DD):"),
                         (self._date_to,   "Hasta (YYYY-MM-DD):")]:
            tk.Label(row, text=lbl, font=s.F_SMALL,
                     bg=s.C_BG_CARD, fg=s.C_GRAY_LT).pack(side="left")
            tk.Entry(row, textvariable=var, width=13, font=s.F_BODY,
                     bg=s.C_BG, relief="flat",
                     highlightbackground=s.C_BORDER,
                     highlightthickness=1).pack(side="left", padx=(2, 10))
            var.trace_add("write", lambda *_: self.on_change())

    # ── toggle colapso ────────────────────────────────────────────────────────
    def _toggle(self, _event=None):
        self._expanded = not self._expanded
        if self._expanded:
            self._body.pack(fill="x")
            self._arrow.config(text="▼")
        else:
            self._body.pack_forget()
            self._arrow.config(text="▶")

    # ── checkboxes con búsqueda ───────────────────────────────────────────────
    def _refresh_checkboxes(self):
        for w in self._cb_scroll.inner.winfo_children():
            w.destroy()
        query = self._search_var.get().lower()
        unique_vals = self.series.dropna().astype(str).unique()
        filtered = [v for v in sorted(unique_vals)
                    if query in v.lower()][:200]  # máx 200 opciones

        for val in filtered:
            if val not in self._check_vars:
                self._check_vars[val] = tk.BooleanVar(value=True)
            var = self._check_vars[val]
            cb = tk.Checkbutton(
                self._cb_scroll.inner, text=val,
                variable=var, bg=s.C_BG_CARD,
                font=s.F_SMALL, fg=s.C_DARK,
                activebackground=s.C_BG_CARD,
                selectcolor=s.C_RED_LT,
                command=self.on_change,
            )
            cb.pack(anchor="w", padx=6, pady=1)

        # Valores no filtrados no mostrados → mantener su estado
        for val in unique_vals:
            if val not in self._check_vars:
                self._check_vars[val] = tk.BooleanVar(value=True)

    def _select_all(self):
        for var in self._check_vars.values():
            var.set(True)
        self.on_change()

    def _deselect_all(self):
        for var in self._check_vars.values():
            var.set(False)
        self.on_change()

    # ── API pública ───────────────────────────────────────────────────────────
    def is_active(self) -> bool:
        if self.kind == "text":
            return any(not v.get() for v in self._check_vars.values())
        if self.kind == "numeric":
            return bool(self._num_min.get() or self._num_max.get())
        if self.kind == "datetime":
            return bool(self._date_from.get() or self._date_to.get())
        return False

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica este filtro al dataframe y devuelve el resultado."""
        col = self.col
        if col not in df.columns:
            return df

        if self.kind == "text":
            excluded = {v for v, var in self._check_vars.items() if not var.get()}
            if excluded:
                df = df[~df[col].astype(str).isin(excluded)]

        elif self.kind == "numeric":
            min_s = self._num_min.get().strip()
            max_s = self._num_max.get().strip()
            if min_s:
                try:
                    df = df[pd.to_numeric(df[col], errors="coerce") >= float(min_s)]
                except ValueError:
                    pass
            if max_s:
                try:
                    df = df[pd.to_numeric(df[col], errors="coerce") <= float(max_s)]
                except ValueError:
                    pass

        elif self.kind == "datetime":
            dt_col = pd.to_datetime(df[col], errors="coerce")
            from_s = self._date_from.get().strip()
            to_s   = self._date_to.get().strip()
            if from_s:
                try:
                    df = df[dt_col >= pd.to_datetime(from_s)]
                except Exception:
                    pass
            if to_s:
                try:
                    df = df[dt_col <= pd.to_datetime(to_s)]
                except Exception:
                    pass

        # Badge de activo
        if self.is_active():
            self._active_badge.pack(side="right", padx=4)
        else:
            self._active_badge.pack_forget()

        return df

    def reset(self):
        for v in self._check_vars.values():
            v.set(True)
        self._num_min.set("")
        self._num_max.set("")
        self._date_from.set("")
        self._date_to.set("")
        self._active_badge.pack_forget()
        self.on_change()


# ─────────────────────────────────────────────────────────────────────────────
#  Fila de criterio de ordenamiento
# ─────────────────────────────────────────────────────────────────────────────

class SortCriterion(tk.Frame):
    def __init__(self, parent, columns: list[str], on_delete, **kw):
        super().__init__(parent, bg=s.C_BG, **kw)
        self._on_delete = on_delete

        self._col_var = tk.StringVar(value=columns[0] if columns else "")
        self._dir_var = tk.StringVar(value="ASC")

        # Combobox columna
        col_cb = ttk.Combobox(self, textvariable=self._col_var,
                              values=columns, state="readonly", width=22,
                              font=s.F_BODY)
        col_cb.pack(side="left", padx=(0, 6))

        # Botones ASC / DESC
        asc_btn  = tk.Button(self, text="↑ ASC",  command=lambda: self._set_dir("ASC"),
                             bg=s.C_RED, fg=s.C_WHITE, font=s.F_BTN_SM,
                             bd=0, padx=8, pady=4, cursor="hand2")
        desc_btn = tk.Button(self, text="↓ DESC", command=lambda: self._set_dir("DESC"),
                             bg=s.C_BG, fg=s.C_GRAY, font=s.F_BTN_SM,
                             bd=0, padx=8, pady=4, cursor="hand2")

        self._btns = {"ASC": asc_btn, "DESC": desc_btn}
        asc_btn.pack(side="left", padx=2)
        desc_btn.pack(side="left", padx=2)

        IconBtn(self, "✕", command=self._delete,
                bg=s.C_BG, fg=s.C_GRAY_LT).pack(side="left", padx=(8, 0))

    def _set_dir(self, direction: str):
        self._dir_var.set(direction)
        for d, btn in self._btns.items():
            if d == direction:
                btn.config(bg=s.C_RED, fg=s.C_WHITE)
            else:
                btn.config(bg=s.C_BG, fg=s.C_GRAY)

    def _delete(self):
        self.destroy()
        if self._on_delete:
            self._on_delete()

    def get(self) -> tuple[str, bool]:
        """Devuelve (col, ascending)."""
        return self._col_var.get(), self._dir_var.get() == "ASC"


# ─────────────────────────────────────────────────────────────────────────────
#  Pantalla principal de Filtrado
# ─────────────────────────────────────────────────────────────────────────────

class FilterScreen(BaseScreen):
    title = "FILTRAR & ORDENAR"

    PREVIEW_ROWS = 50

    def __init__(self, container, router):
        super().__init__(container, router)
        self.df: pd.DataFrame | None = None
        self._filter_panels: list[ColumnFilterPanel] = []
        self._col_vars: dict[str, tk.BooleanVar] = {}
        self._sort_rows: list[SortCriterion] = []

    # ── shell ─────────────────────────────────────────────────────────────────
    def build_body(self, parent):
        # ── Barra superior ────────────────────────────────────────────────────
        action_bar = tk.Frame(parent, bg=s.C_BG, pady=10)
        action_bar.pack(fill="x", padx=s.PAD_LG)

        PrimaryBtn(action_bar, "Abrir archivo",
                   command=self._load_file).pack(side="left")

        self._file_badge = Badge(action_bar, "Sin archivo cargado", kind="neutral")
        self._file_badge.pack(side="left", padx=10)

        self._btn_export = SecondaryBtn(action_bar, "Exportar resultado",
                                        command=self._export, state="disabled")
        self._btn_export.pack(side="right")

        self._btn_reset = GhostBtn(action_bar, "↺ Limpiar filtros",
                                   command=self._reset_all)
        self._btn_reset.pack(side="right", padx=8)

        Divider(parent).pack(fill="x")

        # ── Layout 3 columnas ─────────────────────────────────────────────────
        #   [Columnas] | [Filtros] | [Orden + Preview]
        pane = tk.Frame(parent, bg=s.C_BG)
        pane.pack(fill="both", expand=True, padx=s.PAD_LG, pady=s.PAD_SM)

        # --- Panel 1: Selección de columnas ----------------------------------
        p1 = tk.Frame(pane, bg=s.C_BG, width=190)
        p1.pack(side="left", fill="y", padx=(0, 10))
        p1.pack_propagate(False)

        self._build_columns_panel(p1)

        # --- Panel 2: Filtros ------------------------------------------------
        p2 = tk.Frame(pane, bg=s.C_BG, width=270)
        p2.pack(side="left", fill="y", padx=(0, 10))
        p2.pack_propagate(False)

        self._build_filters_panel(p2)

        # --- Panel 3: Ordenar + Preview --------------------------------------
        p3 = tk.Frame(pane, bg=s.C_BG)
        p3.pack(side="left", fill="both", expand=True)

        self._build_sort_panel(p3)
        self._build_preview_panel(p3)

    # ── Panel 1: Columnas ─────────────────────────────────────────────────────
    def _build_columns_panel(self, parent):
        hdr = tk.Frame(parent, bg=s.C_BG)
        hdr.pack(fill="x", pady=(0, 4))
        tk.Label(hdr, text="COLUMNAS", font=s.F_BTN_SM,
                 bg=s.C_BG, fg=s.C_GRAY_LT).pack(side="left")

        btn_row = tk.Frame(parent, bg=s.C_BG)
        btn_row.pack(fill="x", pady=(0, 4))
        GhostBtn(btn_row, "✓ Todas",
                 command=self._select_all_cols).pack(side="left")
        GhostBtn(btn_row, "✗ Ninguna",
                 command=self._deselect_all_cols).pack(side="left", padx=3)

        self._col_scroll = ScrollableFrame(parent, bg=s.C_BG_CARD)
        self._col_scroll.pack(fill="both", expand=True)

        # Borde en la tarjeta
        outer = tk.Frame(parent,
                         highlightbackground=s.C_BORDER, highlightthickness=1,
                         bg=s.C_BORDER)
        # repack para que el borde envuelva el scrollable
        self._col_scroll.pack_forget()
        outer.pack(fill="both", expand=True)
        self._col_scroll = ScrollableFrame(outer, bg=s.C_BG_CARD)
        self._col_scroll.pack(fill="both", expand=True, padx=1, pady=1)

    # ── Panel 2: Filtros ──────────────────────────────────────────────────────
    def _build_filters_panel(self, parent):
        hdr = tk.Frame(parent, bg=s.C_BG)
        hdr.pack(fill="x", pady=(0, 4))
        tk.Label(hdr, text="FILTROS", font=s.F_BTN_SM,
                 bg=s.C_BG, fg=s.C_GRAY_LT).pack(side="left")
        self._active_count = Badge(hdr, "0 activos", kind="neutral")
        self._active_count.pack(side="left", padx=6)

        outer = tk.Frame(parent,
                         highlightbackground=s.C_BORDER, highlightthickness=1,
                         bg=s.C_BORDER)
        outer.pack(fill="both", expand=True)
        self._filter_scroll = ScrollableFrame(outer, bg=s.C_BG_CARD)
        self._filter_scroll.pack(fill="both", expand=True, padx=1, pady=1)

    # ── Panel 3a: Ordenamiento ────────────────────────────────────────────────
    def _build_sort_panel(self, parent):
        sort_card = Card(parent)
        sort_card.pack(fill="x", pady=(0, 10))

        hdr = tk.Frame(sort_card, bg=s.C_BG_CARD)
        hdr.pack(fill="x")
        tk.Label(hdr, text="ORDENAR POR", font=s.F_BTN_SM,
                 bg=s.C_BG_CARD, fg=s.C_GRAY_LT).pack(side="left")
        GhostBtn(hdr, "＋ Agregar criterio",
                 command=self._add_sort_row).pack(side="right")

        Divider(sort_card).pack(fill="x", pady=6)

        self._sort_container = tk.Frame(sort_card, bg=s.C_BG_CARD)
        self._sort_container.pack(fill="x")

        tk.Label(sort_card, text="Arrastra los criterios para reordenarlos",
                 font=s.F_SMALL, bg=s.C_BG_CARD, fg=s.C_BORDER).pack(anchor="w")

    # ── Panel 3b: Vista previa ────────────────────────────────────────────────
    def _build_preview_panel(self, parent):
        hdr = tk.Frame(parent, bg=s.C_BG)
        hdr.pack(fill="x", pady=(0, 4))
        tk.Label(hdr, text="VISTA PREVIA", font=s.F_BTN_SM,
                 bg=s.C_BG, fg=s.C_GRAY_LT).pack(side="left")
        self._preview_info = Badge(hdr, "—", kind="neutral")
        self._preview_info.pack(side="left", padx=8)

        # Frame para el TreeView
        tree_frame = tk.Frame(parent,
                              highlightbackground=s.C_BORDER, highlightthickness=1,
                              bg=s.C_BORDER)
        tree_frame.pack(fill="both", expand=True)

        # Estilo del treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Filter.Treeview",
                        background=s.C_BG_CARD,
                        foreground=s.C_DARK,
                        rowheight=24,
                        fieldbackground=s.C_BG_CARD,
                        font=s.F_SMALL)
        style.configure("Filter.Treeview.Heading",
                        background=s.C_BG,
                        foreground=s.C_GRAY,
                        font=s.F_BTN_SM,
                        relief="flat")
        style.map("Filter.Treeview",
                  background=[("selected", s.C_RED_LT)],
                  foreground=[("selected", s.C_RED)])

        self._tree = ttk.Treeview(tree_frame, style="Filter.Treeview",
                                  show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical",
                            command=self._tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal",
                            command=self._tree.xview)
        self._tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self._tree.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

    # ── Cargar archivo ────────────────────────────────────────────────────────
    def _load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Excel / CSV", "*.xlsx *.xlsm *.csv")])
        if not path:
            return
        try:
            if path.endswith(".csv"):
                self.df = pd.read_csv(path)
            else:
                # Elegir hoja si hay varias
                xl = pd.ExcelFile(path)
                if len(xl.sheet_names) > 1:
                    sheet = self._ask_sheet(xl.sheet_names)
                    if not sheet:
                        return
                else:
                    sheet = xl.sheet_names[0]
                self.df = xl.parse(sheet)
        except Exception as e:
            messagebox.showerror("Error al cargar", str(e))
            return

        fname = path.split("/")[-1].split("\\")[-1]
        self._file_badge.config(
            text=f"{fname}  ({len(self.df):,} filas × {len(self.df.columns)} cols)",
            **{"fg": s.C_SUCCESS, "bg": "#E6F4ED"})
        self.status.set(f"Cargado: {fname}", f"{len(self.df):,} filas")
        self._btn_export.config(state="normal")

        self._populate_panels()

    def _ask_sheet(self, sheets: list[str]) -> str | None:
        """Ventana modal para elegir hoja."""
        win = tk.Toplevel(self.container)
        win.title("Elegir hoja")
        win.grab_set()
        win.configure(bg=s.C_BG)
        win.geometry("300x300")

        tk.Label(win, text="¿Qué hoja deseas cargar?",
                 font=s.F_BODY, bg=s.C_BG, fg=s.C_DARK).pack(pady=10)

        lb = tk.Listbox(win, font=s.F_BODY, bg=s.C_BG_CARD, bd=0,
                        selectbackground=s.C_RED_LT, selectforeground=s.C_RED)
        lb.pack(fill="both", expand=True, padx=20, pady=6)
        for sh in sheets:
            lb.insert(tk.END, sh)
        lb.selection_set(0)

        result = [None]

        def ok():
            sel = lb.curselection()
            result[0] = sheets[sel[0]] if sel else sheets[0]
            win.destroy()

        PrimaryBtn(win, "Confirmar", command=ok).pack(pady=10)
        win.wait_window()
        return result[0]

    # ── Poblar paneles ────────────────────────────────────────────────────────
    def _populate_panels(self):
        # Limpiar
        for w in self._col_scroll.inner.winfo_children():
            w.destroy()
        for w in self._filter_scroll.inner.winfo_children():
            w.destroy()
        self._filter_panels.clear()
        self._col_vars.clear()

        for col in self.df.columns:
            # Checkbox columna
            var = tk.BooleanVar(value=True)
            self._col_vars[col] = var
            cb = tk.Checkbutton(
                self._col_scroll.inner, text=col,
                variable=var, bg=s.C_BG_CARD,
                font=s.F_BODY, fg=s.C_DARK,
                activebackground=s.C_BG_CARD,
                selectcolor=s.C_RED_LT,
                command=self._on_filter_change,
                wraplength=160, justify="left",
            )
            cb.pack(anchor="w", padx=8, pady=2)

            # Panel de filtro
            panel = ColumnFilterPanel(
                self._filter_scroll.inner,
                col=col,
                series=self.df[col],
                on_change=self._on_filter_change,
            )
            panel.pack(fill="x", pady=1, padx=2)
            Divider(self._filter_scroll.inner).pack(fill="x")
            self._filter_panels.append(panel)

        # Actualizar criterios de ordenamiento con nuevas columnas
        self._refresh_sort_columns()
        self._update_preview()

    # ── Ordenamiento ──────────────────────────────────────────────────────────
    def _get_columns(self) -> list[str]:
        return list(self.df.columns) if self.df is not None else []

    def _add_sort_row(self):
        cols = self._get_columns()
        if not cols:
            return
        row = SortCriterion(self._sort_container, cols,
                            on_delete=self._update_preview)
        row.pack(fill="x", pady=3)
        self._update_preview()

    def _refresh_sort_columns(self):
        """Actualiza los combos de los criterios de orden al cargar nuevos datos."""
        for w in self._sort_container.winfo_children():
            w.destroy()

    # ── Aplicar filtros y orden ───────────────────────────────────────────────
    def _build_result(self) -> pd.DataFrame:
        if self.df is None:
            return pd.DataFrame()

        result = self.df.copy()

        # 1. Filtros por columna
        for panel in self._filter_panels:
            result = panel.apply(result)

        # 2. Ordenamiento múltiple
        sort_criteria = []
        for w in self._sort_container.winfo_children():
            if isinstance(w, SortCriterion):
                col, asc = w.get()
                if col in result.columns:
                    sort_criteria.append((col, asc))
        if sort_criteria:
            by   = [c for c, _ in sort_criteria]
            asc  = [a for _, a in sort_criteria]
            result = result.sort_values(by=by, ascending=asc)

        # 3. Seleccionar columnas activas
        selected = [c for c, v in self._col_vars.items() if v.get()]
        if selected:
            result = result[[c for c in selected if c in result.columns]]

        return result

    def _on_filter_change(self):
        active = sum(1 for p in self._filter_panels if p.is_active())
        self._active_count.config(text=f"{active} activo(s)")
        self._update_preview()

    def _update_preview(self):
        if self.df is None:
            return
        result = self._build_result()
        self._refresh_tree(result.head(self.PREVIEW_ROWS))
        self._preview_info.config(
            text=f"{len(result):,} filas · {len(result.columns)} cols (mostrando {min(len(result), self.PREVIEW_ROWS)})")
        self.status.set(
            f"Resultado: {len(result):,} filas",
            f"Original: {len(self.df):,} filas")

    def _refresh_tree(self, df: pd.DataFrame):
        self._tree.delete(*self._tree.get_children())
        if df.empty:
            self._tree["columns"] = []
            return
        cols = list(df.columns)
        self._tree["columns"] = cols
        for col in cols:
            self._tree.heading(col, text=col)
            self._tree.column(col, width=max(80, len(str(col)) * 9),
                              minwidth=60, stretch=True)
        for _, row in df.iterrows():
            self._tree.insert("", tk.END, values=list(row))

    # ── Limpiar filtros ───────────────────────────────────────────────────────
    def _reset_all(self):
        for panel in self._filter_panels:
            panel.reset()
        for v in self._col_vars.values():
            v.set(True)
        self._active_count.config(text="0 activos")
        self._update_preview()

    # ── Columnas ──────────────────────────────────────────────────────────────
    def _select_all_cols(self):
        for v in self._col_vars.values():
            v.set(True)
        self._on_filter_change()

    def _deselect_all_cols(self):
        for v in self._col_vars.values():
            v.set(False)
        self._on_filter_change()

    # ── Exportar ──────────────────────────────────────────────────────────────
    def _export(self):
        if self.df is None:
            return
        result = self._build_result()
        if result.empty:
            messagebox.showwarning("Sin datos",
                                   "El resultado está vacío con los filtros actuales.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv")])
        if not path:
            return
        try:
            if path.endswith(".csv"):
                result.to_csv(path, index=False)
            else:
                result.to_excel(path, index=False)
            messagebox.showinfo(
                "Exportado",
                f"✓ {len(result):,} filas guardadas en:\n{path}")
            self.status.set("Exportación completada.", f"{len(result):,} filas")
        except Exception as e:
            messagebox.showerror("Error al exportar", str(e))
