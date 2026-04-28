# app/modules/split_sheets.py
"""Módulo: Separar hojas de un Excel en archivos individuales."""

import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

from app.ui import styles as s
from app.ui.components import PrimaryBtn, SecondaryBtn, Divider, Badge, Card
from app.ui.layouts import BaseScreen


class SplitSheetsScreen(BaseScreen):
    title = "SEPARAR SHEETS"

    def __init__(self, container, router):
        super().__init__(container, router)
        self._df_dict: dict = {}
        self._sheet_vars: dict = {}

    def build_body(self, parent):
        action_bar = tk.Frame(parent, bg=s.C_BG, pady=10)
        action_bar.pack(fill="x", padx=s.PAD_LG)
        PrimaryBtn(action_bar, "Abrir archivo Excel",
                   command=self._load).pack(side="left")
        self._btn_run = SecondaryBtn(action_bar, "Separar y guardar",
                                     command=self._run, state="disabled")
        self._btn_run.pack(side="right")

        Divider(parent).pack(fill="x")

        body = tk.Frame(parent, bg=s.C_BG, padx=s.PAD_LG, pady=s.PAD_MD)
        body.pack(fill="both", expand=True)

        tk.Label(body, text="Hojas encontradas:",
                 font=s.F_BTN_SM, bg=s.C_BG, fg=s.C_GRAY_LT).pack(anchor="w")

        self._sheet_card = Card(body)
        self._sheet_card.pack(fill="both", expand=True, pady=8)

        self._info = Badge(body, "Sin archivo", kind="neutral")
        self._info.pack(anchor="w")

    def _load(self):
        path = filedialog.askopenfilename(
            filetypes=[("Excel", "*.xlsx *.xlsm")])
        if not path:
            return
        try:
            self._df_dict = pd.read_excel(path, sheet_name=None)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        for w in self._sheet_card.winfo_children():
            w.destroy()
        self._sheet_vars = {}
        for name in self._df_dict:
            var = tk.BooleanVar(value=True)
            self._sheet_vars[name] = var
            row = tk.Frame(self._sheet_card, bg=s.C_BG_CARD)
            row.pack(fill="x", pady=1)
            tk.Checkbutton(row, text=name, variable=var,
                           font=s.F_BODY, bg=s.C_BG_CARD,
                           fg=s.C_DARK, activebackground=s.C_BG_CARD,
                           selectcolor=s.C_RED_LT).pack(side="left", padx=10)
            nrows = len(self._df_dict[name])
            Badge(row, f"{nrows} filas", kind="info").pack(side="right", padx=10)

        n = len(self._df_dict)
        self._info.config(text=f"{n} hoja(s) disponibles")
        self._btn_run.config(state="normal")
        self.status.set(f"Archivo cargado: {n} hoja(s)")

    def _run(self):
        sel = [n for n, v in self._sheet_vars.items() if v.get()]
        if not sel:
            messagebox.showwarning("Atención", "Selecciona al menos una hoja.")
            return
        folder = filedialog.askdirectory()
        if not folder:
            return
        for name in sel:
            clean = "".join(c for c in name if c.isalnum() or c in " _").strip()
            self._df_dict[name].to_excel(
                os.path.join(folder, f"{clean}.xlsx"), index=False)
        messagebox.showinfo("Éxito", f"{len(sel)} hoja(s) exportadas.")
        self.status.set(f"{len(sel)} archivo(s) guardados.")
