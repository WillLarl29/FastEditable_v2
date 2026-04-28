"""
Script de prueba automática — Simula navegación sin GUI visible.
"""

import sys
import tkinter as tk
from tkinter import simpledialog
import threading
import time

# Importar la aplicación
from app.core.router import Router
from app.modules.menu import MenuScreen
from app.modules.union_sheets import UnionSheetsScreen
from app.modules.merge_files import MergeFilesScreen
from app.modules.split_sheets import SplitSheetsScreen
from app.modules.filter_module import FilterScreen


def test_navigation():
    """Prueba la navegación sin GUI visible."""
    print("\n" + "=" * 70)
    print("🤖 PRUEBA AUTOMÁTICA DE NAVEGACIÓN")
    print("=" * 70 + "\n")

    # Crear ventana invisible
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana

    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    router = Router(container)

    test_cases = [
        ("MenuScreen", MenuScreen),
        ("UnionSheetsScreen", UnionSheetsScreen),
        ("Volver a MenuScreen", MenuScreen),
        ("MergeFilesScreen", MergeFilesScreen),
        ("Volver a MenuScreen", MenuScreen),
        ("SplitSheetsScreen", SplitSheetsScreen),
        ("Volver a MenuScreen", MenuScreen),
        ("FilterScreen", FilterScreen),
        ("Volver a MenuScreen", MenuScreen),
    ]

    all_passed = True
    for i, (description, screen_class) in enumerate(test_cases, 1):
        try:
            router.navigate(screen_class)
            print(f"✅ Test {i}: {description}")
        except Exception as e:
            print(f"❌ Test {i}: {description}")
            print(f"   Error: {e}")
            all_passed = False
            break

    root.destroy()

    print("\n" + "=" * 70)
    if all_passed:
        print("✅ TODAS LAS PRUEBAS PASARON")
        print("   La navegación funciona correctamente.")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
    print("=" * 70 + "\n")

    return all_passed


def test_menu_navigation():
    """Prueba el sistema de navegación del menú."""
    print("\n" + "=" * 70)
    print("🎯 PRUEBA DE RUTAS DEL MENÚ")
    print("=" * 70 + "\n")

    # Importar MenuScreen correctamente
    from app.modules.menu import MenuScreen as TestMenuScreen

    # Crear ventana invisible
    root = tk.Tk()
    root.withdraw()

    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    router = Router(container)
    router.navigate(TestMenuScreen)

    # El router debería haber navegado exitosamente a MenuScreen
    if router._current is not None:
        print("✅ MenuScreen se navegó correctamente")
        print(f"✅ Pantalla actual: {router._current.__class__.__name__}")

        # Probar acceso a ITEMS
        if hasattr(router._current, 'ITEMS'):
            items = router._current.ITEMS
            print(f"✅ ITEMS accesible: {len(items)} módulos disponibles")
            for i, (num, title, desc, route) in enumerate(items, 1):
                print(f"   {num}. {title} ({route})")
        else:
            print("❌ ITEMS no encontrado en MenuScreen")

        print("\n✅ TODAS LAS PRUEBAS DE MENÚ PASARON")
    else:
        print("❌ MenuScreen no se navegó correctamente")

    root.destroy()
    print("=" * 70 + "\n")

    return router._current is not None


if __name__ == "__main__":
    try:
        result1 = test_navigation()
        result2 = test_menu_navigation()

        if result1 and result2:
            print("\n" + "╔" + "=" * 68 + "╗")
            print("║" + " ✅ TODAS LAS PRUEBAS AUTOMÁTICAS PASARON ".center(68) + "║")
            print("║" + " La aplicación está funcionando correctamente ".center(68) + "║")
            print("╚" + "=" * 68 + "╝\n")
            sys.exit(0)
        else:
            print("\n" + "╔" + "=" * 68 + "╗")
            print("║" + " ❌ ALGUNAS PRUEBAS FALLARON ".center(68) + "║")
            print("╚" + "=" * 68 + "╝\n")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ ERROR EN PRUEBAS:\n{e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
