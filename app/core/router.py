# app/core/router.py
"""Gestiona la navegación entre pantallas (módulos)."""


class Router:
    def __init__(self, container):
        self.container = container
        self._current = None

    # ── utilidad interna ──────────────────────────────────────────────────────
    def _clear(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # ── navegación ────────────────────────────────────────────────────────────
    def navigate(self, screen_class, **kwargs):
        """Instancia screen_class(container, router, **kwargs) y llama render()."""
        self._clear()
        self._current = screen_class(self.container, self, **kwargs)
        self._current.render()
