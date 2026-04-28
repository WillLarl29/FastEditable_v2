# app/modules/merge_files.py
"""Módulo: Unir múltiples archivos en uno solo."""

import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

from app.ui import styles as s
from app.ui.components import PrimaryBtn, SecondaryBtn, Divider, Badge
from app.ui.layouts import BaseScreen


class MergeFilesScreen(BaseScreen):
    title = "UNIR ARCHIVOS"

    def __init__(self, container, router):
        super().__init__(container, router)
        self._files: list[str] = []

    def build_body(self, parent):
        action_bar = tk.Frame(parent, bg=s.C_BG, pady=10)
        action_bar.pack(fill="x", padx=s.PAD_LG)
        PrimaryBtn(action_bar, "＋ Seleccionar archivos",
                   command=self._load).pack(side="left")
        self._btn_run = SecondaryBtn(action_bar, "Consolidar y guardar",
                                     command=self._run, state="disabled")
        self._btn_run.pack(side="right")

        Divider(parent).pack(fill="x")

        body = tk.Frame(parent, bg=s.C_BG, padx=s.PAD_LG, pady=s.PAD_MD)
        body.pack(fill="both", expand=True)

        tk.Label(body, text="Archivos seleccionados:",
                 font=s.F_BTN_SM, bg=s.C_BG, fg=s.C_GRAY_LT).pack(anchor="w")

        self._list_frame = tk.Frame(body, bg=s.C_BG_CARD,
                                     highlightbackground=s.C_BORDER,
                                     highlightthickness=1)
        self._list_frame.pack(fill="both", expand=True, pady=8)

        self._count_badge = Badge(body, "0 archivos", kind="neutral")
        self._count_badge.pack(anchor="w")

    def _load(self):
        paths = filedialog.askopenfilenames(
            filetypes=[("Excel/CSV", "*.xlsx *.xlsm *.csv")])
        self._files = list(paths)
        for w in self._list_frame.winfo_children():
            w.destroy()
        for p in self._files:
            tk.Label(self._list_frame, text=f"  ✓  {os.path.basename(p)}",
                     font=s.F_BODY, bg=s.C_BG_CARD, fg=s.C_DARK,
                     anchor="w").pack(fill="x", padx=10, pady=2)
        n = len(self._files)
        self._count_badge.config(text=f"{n} archivo(s) seleccionado(s)")
        if n:
            self._btn_run.config(state="normal")
        self.status.set(f"{n} archivo(s) listos para consolidar")

    def _run(self):
        if not self._files:
            return
        all_dfs = []
        for f in self._files:
            try:
                if f.endswith(".csv"):
                    all_dfs.append(pd.read_csv(f))
                else:
                    sheets = pd.read_excel(f, sheet_name=None)
                    all_dfs.append(pd.concat(sheets.values(), ignore_index=True))
            except Exception as e:
                messagebox.showerror("Error", f"{os.path.basename(f)}: {e}")
                return
        final = pd.concat(all_dfs, ignore_index=True)
        path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                            filetypes=[("Excel", "*.xlsx")])
        if path:
            final.to_excel(path, index=False)
            messagebox.showinfo("Éxito", f"Guardado: {len(final)} filas totales.")
            self.status.set(f"Consolidado: {len(final)} filas.")
