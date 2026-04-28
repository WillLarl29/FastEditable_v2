# app/modules/union_sheets.py
"""Módulo: Unir hojas de múltiples archivos Excel."""

import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from app.ui import styles as s
from app.ui.components import PrimaryBtn, SecondaryBtn, Card, ScrollableFrame, Divider
from app.ui.layouts import BaseScreen


class UnionSheetsScreen(BaseScreen):
    title = "UNIR SHEETS"

    def __init__(self, container, router):
        super().__init__(container, router)
        self.batch_files: dict = {}  # path -> {sheets, vars, out_name}
        self._sel_path: str | None = None

    # ── cuerpo ────────────────────────────────────────────────────────────────
    def build_body(self, parent):
        # Barra de acciones superior
        action_bar = tk.Frame(parent, bg=s.C_BG, pady=10)
        action_bar.pack(fill="x", padx=s.PAD_LG)

        PrimaryBtn(action_bar, "＋ Cargar archivos",
                   command=self._load_files).pack(side="left")

        self._btn_process = SecondaryBtn(action_bar, "Consolidar y guardar todo",
                                         command=self._process, state="disabled")
        self._btn_process.pack(side="right")

        Divider(parent).pack(fill="x")

        # Cuerpo dividido
        pane = tk.Frame(parent, bg=s.C_BG)
        pane.pack(fill="both", expand=True, padx=s.PAD_LG, pady=s.PAD_MD)

        # ── Lista de archivos (izquierda) ─────────────────────────────────────
        left = tk.Frame(pane, bg=s.C_BG, width=260)
        left.pack(side="left", fill="y", padx=(0, 12))
        left.pack_propagate(False)

        tk.Label(left, text="ARCHIVOS CARGADOS", font=s.F_BTN_SM,
                 bg=s.C_BG, fg=s.C_GRAY_LT).pack(anchor="w", pady=(0, 6))

        list_card = Card(left, padx=0, pady=0)
        list_card.pack(fill="both", expand=True)

        self._listbox = tk.Listbox(list_card, bg=s.C_BG_CARD, bd=0,
                                   font=s.F_BODY, fg=s.C_DARK,
                                   selectbackground=s.C_RED_LT,
                                   selectforeground=s.C_RED,
                                   activestyle="none")
        self._listbox.pack(fill="both", expand=True, padx=2, pady=2)
        self._listbox.bind("<<ListboxSelect>>", self._on_select)

        # ── Configuración (derecha) ───────────────────────────────────────────
        right = tk.Frame(pane, bg=s.C_BG)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(right, text="CONFIGURACIÓN DE SALIDA", font=s.F_BTN_SM,
                 bg=s.C_BG, fg=s.C_GRAY_LT).pack(anchor="w", pady=(0, 6))

        cfg_card = Card(right)
        cfg_card.pack(fill="both", expand=True)

        tk.Label(cfg_card, text="Nombre del archivo de salida:",
                 font=s.F_BODY, bg=s.C_BG_CARD, fg=s.C_GRAY).pack(anchor="w")

        self._out_entry = tk.Entry(cfg_card, font=s.F_BODY,
                                   bg=s.C_BG, relief="flat",
                                   highlightbackground=s.C_BORDER,
                                   highlightthickness=1)
        self._out_entry.pack(fill="x", pady=(4, 12))
        self._out_entry.bind("<KeyRelease>", self._update_out_name)

        tk.Label(cfg_card, text="Hojas a incluir:",
                 font=s.F_BODY, bg=s.C_BG_CARD, fg=s.C_GRAY).pack(anchor="w")

        self._sheets_scroll = ScrollableFrame(cfg_card, bg=s.C_BG_CARD)
        self._sheets_scroll.pack(fill="both", expand=True, pady=(4, 0))

    # ── helpers ───────────────────────────────────────────────────────────────
    def _load_files(self):
        paths = filedialog.askopenfilenames(
            filetypes=[("Archivos de datos", "*.xlsx *.xlsm *.csv")])
        for p in paths:
            if p in self.batch_files:
                continue
            fname = os.path.basename(p)
            try:
                data = (pd.read_excel(p, sheet_name=None)
                        if not p.endswith(".csv")
                        else {"CSV": pd.read_csv(p)})
                self.batch_files[p] = {
                    "sheets":   data,
                    "vars":     {n: tk.BooleanVar(value=True) for n in data},
                    "out_name": fname.rsplit(".", 1)[0] + "_UNIDO",
                }
                self._listbox.insert(tk.END, f"  {fname}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir {fname}:\n{e}")

        if self.batch_files:
            self._btn_process.config(state="normal")
            self.status.set(f"{len(self.batch_files)} archivo(s) cargado(s)")

    def _on_select(self, _event):
        idx = self._listbox.curselection()
        if not idx:
            return
        path = list(self.batch_files.keys())[idx[0]]
        self._sel_path = path
        info = self.batch_files[path]

        self._out_entry.delete(0, tk.END)
        self._out_entry.insert(0, info["out_name"])

        # Refrescar checkboxes de hojas
        for w in self._sheets_scroll.inner.winfo_children():
            w.destroy()
        for name, var in info["vars"].items():
            tk.Checkbutton(self._sheets_scroll.inner, text=name,
                           variable=var, bg=s.C_BG_CARD,
                           font=s.F_BODY, fg=s.C_DARK,
                           activebackground=s.C_BG_CARD,
                           selectcolor=s.C_RED_LT).pack(anchor="w", pady=1)

    def _update_out_name(self, _):
        if self._sel_path and self._sel_path in self.batch_files:
            self.batch_files[self._sel_path]["out_name"] = self._out_entry.get()

    def _process(self):
        if not self.batch_files:
            return
        folder = filedialog.askdirectory()
        if not folder:
            return
        errors = []
        for path, info in self.batch_files.items():
            selected = [n for n, v in info["vars"].items() if v.get()]
            if not selected:
                continue
            try:
                df = pd.concat([info["sheets"][n] for n in selected], ignore_index=True)
                out = os.path.join(folder, f"{info['out_name']}.xlsx")
                df.to_excel(out, index=False)
            except Exception as e:
                errors.append(f"{os.path.basename(path)}: {e}")

        if errors:
            messagebox.showerror("Errores", "\n".join(errors))
        else:
            messagebox.showinfo("Éxito", f"Proceso completado — {len(self.batch_files)} archivo(s) guardado(s).")
            self.status.set("Consolidación completada.")
