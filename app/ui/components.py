# app/ui/components.py
"""Widgets reutilizables de alto nivel."""

import tkinter as tk
from tkinter import ttk
from . import styles as s


# ─────────────────────────────────────────────────────────────────────────────
#  Botones
# ─────────────────────────────────────────────────────────────────────────────

class PrimaryBtn(tk.Button):
    def __init__(self, parent, text, command=None, width=None, **kw):
        opts = dict(
            text=text, command=command,
            bg=s.C_RED, fg=s.C_WHITE, activebackground=s.C_RED_DK,
            font=s.F_BTN, bd=0, cursor="hand2",
            padx=20, pady=10, relief="flat",
        )
        if width: opts["width"] = width
        opts.update(kw)
        super().__init__(parent, **opts)
        self.bind("<Enter>", lambda e: self.config(bg=s.C_RED_DK))
        self.bind("<Leave>", lambda e: self.config(bg=s.C_RED))


class SecondaryBtn(tk.Button):
    def __init__(self, parent, text, command=None, width=None, **kw):
        opts = dict(
            text=text, command=command,
            bg=s.C_BG_CARD, fg=s.C_GRAY, activebackground=s.C_BG,
            font=s.F_BTN, bd=1, relief="solid", cursor="hand2",
            padx=18, pady=9,
        )
        if width: opts["width"] = width
        opts.update(kw)
        super().__init__(parent, **opts)
        self.bind("<Enter>", lambda e: self.config(bg=s.C_BG))
        self.bind("<Leave>", lambda e: self.config(bg=s.C_BG_CARD))


class GhostBtn(tk.Button):
    def __init__(self, parent, text, command=None, **kw):
        opts = dict(
            text=text, command=command,
            bg=s.C_BG, fg=s.C_GRAY, activebackground=s.C_BORDER,
            font=s.F_BTN_SM, bd=0, cursor="hand2",
            padx=12, pady=6, relief="flat",
        )
        opts.update(kw)
        super().__init__(parent, **opts)


class BackBtn(tk.Button):
    def __init__(self, parent, command=None, **kw):
        opts = dict(
            text="← VOLVER", command=command,
            bg=s.C_BG, fg=s.C_GRAY_LT, activebackground=s.C_BORDER,
            font=s.F_BTN_SM, bd=0, cursor="hand2",
            padx=10, pady=6, relief="flat",
        )
        opts.update(kw)
        super().__init__(parent, **opts)
        self.bind("<Enter>", lambda e: self.config(fg=s.C_GRAY))
        self.bind("<Leave>", lambda e: self.config(fg=s.C_GRAY_LT))


class IconBtn(tk.Button):
    """Botón pequeño cuadrado (icono de texto)."""
    def __init__(self, parent, symbol, command=None, bg=None, fg=None, **kw):
        _bg = bg or s.C_BG
        _fg = fg or s.C_GRAY
        opts = dict(
            text=symbol, command=command,
            bg=_bg, fg=_fg, activebackground=s.C_BORDER,
            font=("Segoe UI", 10), bd=0, cursor="hand2",
            padx=6, pady=4, relief="flat", width=3,
        )
        opts.update(kw)
        super().__init__(parent, **opts)


# ─────────────────────────────────────────────────────────────────────────────
#  Etiquetas
# ─────────────────────────────────────────────────────────────────────────────

class H1(tk.Label):
    def __init__(self, parent, text, **kw):
        super().__init__(parent, text=text, font=s.F_H1, bg=s.C_BG, fg=s.C_DARK, **kw)


class H2(tk.Label):
    def __init__(self, parent, text, **kw):
        super().__init__(parent, text=text, font=s.F_H2, bg=s.C_BG, fg=s.C_GRAY, **kw)


class BodyLabel(tk.Label):
    def __init__(self, parent, text, bg=None, **kw):
        super().__init__(parent, text=text, font=s.F_BODY, bg=bg or s.C_BG, fg=s.C_GRAY, **kw)


class Badge(tk.Label):
    """Etiqueta de chip coloreado."""
    COLORS = {
        "success": (s.C_SUCCESS, "#E6F4ED"),
        "warn":    (s.C_WARN,    "#FEF3C7"),
        "info":    (s.C_INFO,    "#DBEAFE"),
        "neutral": (s.C_GRAY,    s.C_BG),
        "red":     (s.C_RED,     s.C_RED_LT),
    }
    def __init__(self, parent, text, kind="neutral", **kw):
        fg, bg = self.COLORS.get(kind, self.COLORS["neutral"])
        super().__init__(parent, text=text, font=s.F_SMALL,
                         fg=fg, bg=bg, padx=6, pady=2, **kw)


# ─────────────────────────────────────────────────────────────────────────────
#  Separador
# ─────────────────────────────────────────────────────────────────────────────

class Divider(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, height=1, bg=s.C_BORDER, **kw)


# ─────────────────────────────────────────────────────────────────────────────
#  Card (frame con fondo blanco y borde sutil)
# ─────────────────────────────────────────────────────────────────────────────

class Card(tk.Frame):
    def __init__(self, parent, **kw):
        # Extraer padx y pady de kw si existen, sino usar valores por defecto
        padx = kw.pop("padx", s.PAD_MD)
        pady = kw.pop("pady", s.PAD_MD)
        super().__init__(parent, bg=s.C_BG_CARD,
                         highlightbackground=s.C_BORDER,
                         highlightthickness=1,
                         padx=padx, pady=pady, **kw)


# ─────────────────────────────────────────────────────────────────────────────
#  ScrollableFrame
# ─────────────────────────────────────────────────────────────────────────────

class ScrollableFrame(tk.Frame):
    """Frame con scrollbar vertical interno."""
    def __init__(self, parent, bg=None, **kw):
        _bg = bg or s.C_BG_CARD
        super().__init__(parent, bg=_bg, **kw)

        self.canvas = tk.Canvas(self, bg=_bg, bd=0, highlightthickness=0)
        sb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=_bg)

        self.inner.bind("<Configure>",
                        lambda e: self.canvas.config(
                            scrollregion=self.canvas.bbox("all")))

        self._win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.itemconfig(self._win, width=e.width))

        self.canvas.configure(yscrollcommand=sb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Scroll: un handler global que delega al ScrollableFrame más cercano al cursor
        self.canvas.bind_all("<MouseWheel>", ScrollableFrame._route_scroll)

    @staticmethod
    def _route_scroll(event):
        """Sube la jerarquía del widget bajo el cursor y scrollea el ScrollableFrame más cercano."""
        w = event.widget
        while w is not None:
            if isinstance(w, ScrollableFrame):
                w.canvas.yview_scroll(-1 * (event.delta // 120), "units")
                return
            try:
                parent_path = w.winfo_parent()
                if not parent_path:
                    break
                w = w.nametowidget(parent_path)
            except Exception:
                break


# ─────────────────────────────────────────────────────────────────────────────
#  StatusBar
# ─────────────────────────────────────────────────────────────────────────────

class StatusBar(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=s.C_DARK, pady=4, **kw)
        self._lbl = tk.Label(self, text="Listo", font=s.F_SMALL,
                             bg=s.C_DARK, fg=s.C_GRAY_LT)
        self._lbl.pack(side="left", padx=12)
        self._right = tk.Label(self, text="", font=s.F_SMALL,
                               bg=s.C_DARK, fg=s.C_GRAY_LT)
        self._right.pack(side="right", padx=12)

    def set(self, msg, right=""):
        self._lbl.config(text=msg)
        self._right.config(text=right)
