# app/modules/normalizer.py
"""Módulo: Normalizar valores — detecta y unifica variantes de texto similares."""

import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

from app.ui import styles as s
from app.ui.components import (
    PrimaryBtn, SecondaryBtn, GhostBtn,
    Card, ScrollableFrame, Divider, Badge,
)
from app.ui.layouts import BaseScreen


def _norm_key(val: str) -> str:
    return val.strip().lower()


class NormalizerScreen(BaseScreen):
    title = "NORMALIZAR DATOS"

    def __init__(self, container, router):
        super().__init__(container, router)
        self.df: pd.DataFrame | None = None
        self._selected_col: str | None = None
        self._groups: dict = {}
        self._variant_vars: dict = {}

    # ── shell ─────────────────────────────────────────────────────────────────
    def build_body(self, parent):
        # Barra superior
        action_bar = tk.Frame(parent, bg=s.C_BG, pady=10)
        action_bar.pack(fill="x", padx=s.PAD_LG)

        PrimaryBtn(action_bar, "Abrir archivo", command=self._load_file).pack(side="left")
        self._file_badge = Badge(action_bar, "Sin archivo cargado", kind="neutral")
        self._file_badge.pack(side="left", padx=10)

        self._btn_export = SecondaryBtn(action_bar, "Exportar resultado",
                                        command=self._export, state="disabled")
        self._btn_export.pack(side="right")

        Divider(parent).pack(fill="x")

        # Layout 3 columnas
        pane = tk.Frame(parent, bg=s.C_BG)
        pane.pack(fill="both", expand=True, padx=s.PAD_LG, pady=s.PAD_SM)

        p1 = tk.Frame(pane, bg=s.C_BG, width=175)
        p1.pack(side="left", fill="y", padx=(0, 10))
        p1.pack_propagate(False)
        self._build_columns_panel(p1)

        p2 = tk.Frame(pane, bg=s.C_BG, width=310)
        p2.pack(side="left", fill="y", padx=(0, 10))
        p2.pack_propagate(False)
        self._build_groups_panel(p2)

        p3 = tk.Frame(pane, bg=s.C_BG)
        p3.pack(side="left", fill="both", expand=True)
        self._build_editor_panel(p3)

    # ── Panel 1: columnas ─────────────────────────────────────────────────────
    def _build_columns_panel(self, parent):
        tk.Label(parent, text="COLUMNAS", font=s.F_BTN_SM,
                 bg=s.C_BG, fg=s.C_GRAY_LT).pack(anchor="w", pady=(0, 6))

        outer = tk.Frame(parent, highlightbackground=s.C_BORDER,
                         highlightthickness=1, bg=s.C_BORDER)
        outer.pack(fill="both", expand=True)

        self._col_listbox = tk.Listbox(
            outer, bg=s.C_BG_CARD, bd=0, font=s.F_BODY,
            fg=s.C_DARK, selectbackground=s.C_RED_LT,
            selectforeground=s.C_RED, activestyle="none", relief="flat",
        )
        self._col_listbox.pack(fill="both", expand=True, padx=1, pady=1)
        self._col_listbox.bind("<<ListboxSelect>>", self._on_col_select)

    # ── Panel 2: grupos de variantes ──────────────────────────────────────────
    def _build_groups_panel(self, parent):
        hdr = tk.Frame(parent, bg=s.C_BG)
        hdr.pack(fill="x", pady=(0, 4))
        tk.Label(hdr, text="VALORES SIMILARES", font=s.F_BTN_SM,
                 bg=s.C_BG, fg=s.C_GRAY_LT).pack(side="left")
        self._groups_badge = Badge(hdr, "—", kind="neutral")
        self._groups_badge.pack(side="left", padx=6)

        # Buscador
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._refresh_groups_list())
        search_e = tk.Entry(parent, textvariable=self._search_var,
                            font=s.F_BODY, bg=s.C_BG_CARD,
                            relief="flat", highlightbackground=s.C_BORDER,
                            highlightthickness=1)
        search_e.pack(fill="x", ipady=5, pady=(0, 2))
        tk.Label(parent, text="Buscar en grupos...", font=s.F_SMALL,
                 bg=s.C_BG, fg=s.C_GRAY_LT).pack(anchor="w", pady=(0, 6))

        outer = tk.Frame(parent, highlightbackground=s.C_BORDER,
                         highlightthickness=1, bg=s.C_BORDER)
        outer.pack(fill="both", expand=True)
        self._groups_scroll = ScrollableFrame(outer, bg=s.C_BG_CARD)
        self._groups_scroll.pack(fill="both", expand=True, padx=1, pady=1)

    # ── Panel 3: editor ───────────────────────────────────────────────────────
    def _build_editor_panel(self, parent):
        tk.Label(parent, text="EDITOR DE NORMALIZACIÓN", font=s.F_BTN_SM,
                 bg=s.C_BG, fg=s.C_GRAY_LT).pack(anchor="w", pady=(0, 6))

        self._editor_card = Card(parent)
        self._editor_card.pack(fill="both", expand=True)

        # Placeholder
        self._placeholder = tk.Label(
            self._editor_card,
            text="← Selecciona un grupo de valores para editar",
            font=s.F_BODY, bg=s.C_BG_CARD, fg=s.C_GRAY_LT,
        )
        self._placeholder.pack(expand=True)

        # Contenido del editor (oculto inicialmente)
        self._editor_inner = tk.Frame(self._editor_card, bg=s.C_BG_CARD)

        self._group_title = tk.Label(
            self._editor_inner, text="", font=s.F_H1,
            bg=s.C_BG_CARD, fg=s.C_DARK, wraplength=420, justify="left",
        )
        self._group_title.pack(anchor="w", pady=(0, 4))

        self._group_info = Badge(self._editor_inner, "", kind="warn")
        self._group_info.pack(anchor="w", pady=(0, 10))

        Divider(self._editor_inner).pack(fill="x", pady=(0, 12))

        # Campo "normalizar a:"
        tk.Label(self._editor_inner, text="Normalizar a:",
                 font=s.F_BTN_SM, bg=s.C_BG_CARD, fg=s.C_GRAY).pack(anchor="w")
        self._replace_var = tk.StringVar()
        self._replace_entry = tk.Entry(
            self._editor_inner, textvariable=self._replace_var,
            font=("Segoe UI", 13), bg=s.C_BG,
            relief="flat", highlightbackground=s.C_RED, highlightthickness=2,
        )
        self._replace_entry.pack(fill="x", pady=(4, 16), ipady=7)

        # Variantes con checkboxes
        tk.Label(self._editor_inner, text="Variantes encontradas — selecciona cuáles reemplazar:",
                 font=s.F_BTN_SM, bg=s.C_BG_CARD, fg=s.C_GRAY_LT).pack(anchor="w")

        btn_row = tk.Frame(self._editor_inner, bg=s.C_BG_CARD)
        btn_row.pack(fill="x", pady=(4, 6))
        GhostBtn(btn_row, "✓ Todas", command=self._select_all_variants).pack(side="left")
        GhostBtn(btn_row, "✗ Ninguna", command=self._deselect_all_variants).pack(side="left", padx=4)

        v_outer = tk.Frame(self._editor_inner, bg=s.C_BG_CARD,
                           highlightbackground=s.C_BORDER, highlightthickness=1)
        v_outer.pack(fill="both", expand=True, pady=(0, 16))
        self._variant_scroll = ScrollableFrame(v_outer, bg=s.C_BG_CARD)
        self._variant_scroll.pack(fill="both", expand=True, padx=1, pady=1)

        # Botones de acción
        btn_f = tk.Frame(self._editor_inner, bg=s.C_BG_CARD)
        btn_f.pack(fill="x")
        PrimaryBtn(btn_f, "Aplicar a seleccionadas",
                   command=self._apply_selected).pack(side="left")
        SecondaryBtn(btn_f, "Aplicar a todas las variantes",
                     command=self._apply_all).pack(side="left", padx=10)

    # ── Cargar archivo ────────────────────────────────────────────────────────
    def _load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Excel / CSV", "*.xlsx *.xlsm *.csv")])
        if not path:
            return
        try:
            if path.endswith(".csv"):
                df = pd.read_csv(path)
            else:
                xl = pd.ExcelFile(path)
                sheet = xl.sheet_names[0]
                if len(xl.sheet_names) > 1:
                    sheet = self._ask_sheet(xl.sheet_names) or sheet
                df = xl.parse(sheet)
        except Exception as e:
            messagebox.showerror("Error al cargar", str(e))
            return

        self.df = df.copy()
        fname = os.path.basename(path)
        self._file_badge.config(
            text=f"{fname}  ({len(df):,} filas × {len(df.columns)} cols)",
            fg=s.C_SUCCESS, bg="#E6F4ED")
        self.status.set(f"Cargado: {fname}", f"{len(df):,} filas")
        self._btn_export.config(state="normal")

        self._col_listbox.delete(0, tk.END)
        for col in df.columns:
            self._col_listbox.insert(tk.END, f"  {col}")
        self._selected_col = None
        self._groups.clear()
        self._clear_groups_list()
        self._hide_editor()

    def _ask_sheet(self, sheets):
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

    # ── Análisis de columna ───────────────────────────────────────────────────
    def _on_col_select(self, _event=None):
        idx = self._col_listbox.curselection()
        if not idx or self.df is None:
            return
        col = self.df.columns[idx[0]]
        self._selected_col = col
        self._analyze_column(col)
        self._hide_editor()

    def _analyze_column(self, col: str):
        series = self.df[col].dropna().astype(str)
        raw_groups: dict = {}
        for val in series:
            key = _norm_key(val)
            raw_groups.setdefault(key, {})
            raw_groups[key][val] = raw_groups[key].get(val, 0) + 1

        # Solo grupos con más de 1 variante distinta
        self._groups = {
            k: {"variants": v, "total": sum(v.values())}
            for k, v in raw_groups.items()
            if len(v) > 1
        }
        self._refresh_groups_list()

    def _refresh_groups_list(self):
        for w in self._groups_scroll.inner.winfo_children():
            w.destroy()

        query = self._search_var.get().strip().lower()
        filtered = {
            k: v for k, v in self._groups.items()
            if not query or query in k
        }

        n = len(filtered)
        if n:
            self._groups_badge.config(text=f"{n} grupo(s)",
                                      fg=s.C_RED, bg=s.C_RED_LT)
        else:
            self._groups_badge.config(text="Sin variantes", fg=s.C_GRAY, bg=s.C_BG)

        if not filtered:
            msg = "Sin variantes encontradas" if self._selected_col else "Selecciona una columna"
            tk.Label(self._groups_scroll.inner, text=msg,
                     font=s.F_SMALL, bg=s.C_BG_CARD, fg=s.C_GRAY_LT).pack(pady=20)
            return

        for key, info in sorted(filtered.items()):
            self._make_group_row(key, info)

    def _make_group_row(self, key: str, info: dict):
        row = tk.Frame(self._groups_scroll.inner, bg=s.C_BG_CARD)
        row.pack(fill="x", pady=1, padx=2)

        card = tk.Frame(row, bg=s.C_BG_CARD,
                        highlightbackground=s.C_BORDER, highlightthickness=1,
                        cursor="hand2")
        card.pack(fill="x")

        top = tk.Frame(card, bg=s.C_BG_CARD, pady=7, padx=10, cursor="hand2")
        top.pack(fill="x")

        # Nombre del grupo (valor normalizado)
        tk.Label(top, text=key, font=s.F_BODY, bg=s.C_BG_CARD,
                 fg=s.C_DARK, cursor="hand2", anchor="w").pack(side="left")
        Badge(top, f"{len(info['variants'])} var · {info['total']} filas",
              kind="warn").pack(side="right")

        # Sub-fila con las variantes en pequeño
        preview_vals = list(info["variants"].keys())[:3]
        preview_text = "  →  " + "  |  ".join(f'"{v}"' for v in preview_vals)
        if len(info["variants"]) > 3:
            preview_text += f"  +{len(info['variants']) - 3} más"
        tk.Label(card, text=preview_text, font=s.F_SMALL,
                 bg=s.C_BG_CARD, fg=s.C_GRAY_LT,
                 anchor="w", cursor="hand2").pack(fill="x", padx=10, pady=(0, 6))

        def on_enter(e, c=card):
            c.config(highlightbackground=s.C_RED, highlightthickness=2)
        def on_leave(e, c=card):
            c.config(highlightbackground=s.C_BORDER, highlightthickness=1)
        def on_click(e, k=key, i=info):
            self._open_editor(k, i)

        for w in card.winfo_children() + [card]:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", on_click)
        for w in top.winfo_children():
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", on_click)

    # ── Editor ────────────────────────────────────────────────────────────────
    def _open_editor(self, key: str, info: dict):
        self._variant_vars.clear()

        best = max(info["variants"], key=info["variants"].get)
        self._replace_var.set(best)

        self._group_title.config(text=f'"{key}"')
        self._group_info.config(
            text=f"{info['total']} ocurrencias · {len(info['variants'])} variantes distintas")

        for w in self._variant_scroll.inner.winfo_children():
            w.destroy()

        for variant, count in sorted(info["variants"].items(), key=lambda x: -x[1]):
            var = tk.BooleanVar(value=True)
            self._variant_vars[variant] = var

            row = tk.Frame(self._variant_scroll.inner, bg=s.C_BG_CARD)
            row.pack(fill="x", pady=3, padx=8)

            tk.Checkbutton(row, text=variant, variable=var,
                           font=s.F_BODY, bg=s.C_BG_CARD, fg=s.C_DARK,
                           activebackground=s.C_BG_CARD, selectcolor=s.C_RED_LT,
                           anchor="w").pack(side="left")
            Badge(row, f"{count} fila(s)", kind="neutral").pack(side="right")

        self._show_editor()

    def _show_editor(self):
        self._placeholder.pack_forget()
        self._editor_inner.pack(fill="both", expand=True)

    def _hide_editor(self):
        self._editor_inner.pack_forget()
        self._placeholder.pack(expand=True)

    def _select_all_variants(self):
        for v in self._variant_vars.values():
            v.set(True)

    def _deselect_all_variants(self):
        for v in self._variant_vars.values():
            v.set(False)

    # ── Aplicar reemplazo ─────────────────────────────────────────────────────
    def _apply_selected(self):
        selected = [v for v, var in self._variant_vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("Atención", "Selecciona al menos una variante.")
            return
        self._do_replace(selected)

    def _apply_all(self):
        self._do_replace(list(self._variant_vars.keys()))

    def _do_replace(self, variants: list[str]):
        if not variants or self._selected_col is None or self.df is None:
            return
        new_val = self._replace_var.get()
        if not new_val.strip():
            messagebox.showwarning("Atención", "Escribe el valor de reemplazo.")
            return

        col = self._selected_col
        mask = self.df[col].astype(str).isin(variants)
        n_changed = int(mask.sum())
        self.df.loc[mask, col] = new_val

        self._analyze_column(col)
        self._hide_editor()
        self.status.set(f"{n_changed} celdas actualizadas en '{col}'.",
                        f"→ \"{new_val}\"")
        messagebox.showinfo("Aplicado",
                            f"✓ {n_changed} celda(s) reemplazadas por \"{new_val}\"")

    # ── Limpiar ───────────────────────────────────────────────────────────────
    def _clear_groups_list(self):
        for w in self._groups_scroll.inner.winfo_children():
            w.destroy()
        self._groups_badge.config(text="—", fg=s.C_GRAY, bg=s.C_BG)

    # ── Exportar ──────────────────────────────────────────────────────────────
    def _export(self):
        if self.df is None:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv")],
        )
        if not path:
            return
        try:
            if path.endswith(".csv"):
                self.df.to_csv(path, index=False)
            else:
                self.df.to_excel(path, index=False)
            messagebox.showinfo("Exportado",
                                f"✓ {len(self.df):,} filas guardadas en:\n{path}")
            self.status.set("Exportación completada.", f"{len(self.df):,} filas")
        except Exception as e:
            messagebox.showerror("Error al exportar", str(e))
