"""
Script de prueba interactivo — Ejecuta el programa y permite probar la navegación.
"""

import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox

# Importar la aplicación
from app.core.config import APP_TITLE, APP_WIDTH, APP_HEIGHT
from app.core.router import Router
from app.ui import styles as s
from app.modules.menu import MenuScreen


def run_app():
    """Ejecuta la aplicación y la cierra después de 15 segundos si no se cierra manualmente."""
    app_root = tk.Tk()
    app_root.title(APP_TITLE)
    app_root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
    app_root.configure(bg=s.C_BG)
    app_root.minsize(860, 600)

    # Contenedor raíz para el router
    container = tk.Frame(app_root, bg=s.C_BG)
    container.pack(fill="both", expand=True)

    router = Router(container)
    router.navigate(MenuScreen)

    # Auto-cerrar después de 45 segundos (para CI/CD)
    def auto_close():
        time.sleep(45)
        try:
            app_root.quit()
        except:
            pass

    closer_thread = threading.Thread(daemon=True, target=auto_close)
    closer_thread.start()

    print("=" * 60)
    print("✅ PROGRAMA INICIADO CORRECTAMENTE")
    print("=" * 60)
    print("La ventana debería estar visible.")
    print("Puedes probar:")
    print("  1. Clickear en las tarjetas del menú")
    print("  2. Usar el botón '← VOLVER' para regresar")
    print("  3. Cerrar manualmente la ventana")
    print("\nLa ventana se cerrará automáticamente en 45 segundos...")
    print("=" * 60 + "\n")

    app_root.mainloop()

    print("\n✅ PROGRAMA CERRADO CORRECTAMENTE\n")


if __name__ == "__main__":
    try:
        run_app()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR AL EJECUTAR EL PROGRAMA:\n{e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
