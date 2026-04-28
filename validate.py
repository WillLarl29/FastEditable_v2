"""
Script de validación — Verifica que toda la aplicación esté correctamente configurada.
No ejecuta la GUI, solo valida importaciones y estructura.
"""

import sys
import traceback

def test_imports():
    """Prueba que todos los módulos se importen correctamente."""
    print("=" * 60)
    print("🔍 VALIDACIÓN DE IMPORTACIONES")
    print("=" * 60)
    
    tests = [
        ("app.core.config", ["APP_TITLE", "APP_WIDTH", "APP_HEIGHT"]),
        ("app.core.router", ["Router"]),
        ("app.ui.styles", ["C_RED", "F_H1", "C_BG"]),
        ("app.ui.components", ["PrimaryBtn", "SecondaryBtn", "Card"]),
        ("app.ui.layouts", ["BaseScreen"]),
        ("app.modules.menu", ["MenuScreen"]),
        ("app.modules.union_sheets", ["UnionSheetsScreen"]),
        ("app.modules.merge_files", ["MergeFilesScreen"]),
        ("app.modules.split_sheets", ["SplitSheetsScreen"]),
        ("app.modules.filter_module", ["FilterScreen"]),
    ]
    
    all_ok = True
    for module_name, attrs in tests:
        try:
            module = __import__(module_name, fromlist=attrs)
            for attr in attrs:
                if not hasattr(module, attr):
                    print(f"❌ {module_name}.{attr} — NO ENCONTRADO")
                    all_ok = False
                else:
                    print(f"✅ {module_name}.{attr}")
        except Exception as e:
            print(f"❌ {module_name} — ERROR: {e}")
            traceback.print_exc()
            all_ok = False
    
    return all_ok


def test_screen_instantiation():
    """Prueba que las pantallas se puedan instanciar sin errores."""
    print("\n" + "=" * 60)
    print("🖼️  VALIDACIÓN DE PANTALLAS")
    print("=" * 60)
    
    try:
        import tkinter as tk
        from app.core.router import Router
        from app.modules.menu import MenuScreen
        from app.modules.union_sheets import UnionSheetsScreen
        from app.modules.merge_files import MergeFilesScreen
        from app.modules.split_sheets import SplitSheetsScreen
        from app.modules.filter_module import FilterScreen
        
        # Crear ventana temporal
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana
        
        container = tk.Frame(root)
        container.pack(fill="both", expand=True)
        
        router = Router(container)
        
        screens = [
            ("MenuScreen", MenuScreen),
            ("UnionSheetsScreen", UnionSheetsScreen),
            ("MergeFilesScreen", MergeFilesScreen),
            ("SplitSheetsScreen", SplitSheetsScreen),
            ("FilterScreen", FilterScreen),
        ]
        
        all_ok = True
        for screen_name, screen_class in screens:
            try:
                screen = screen_class(container, router)
                screen.render()
                print(f"✅ {screen_name} — OK")
                # Limpiar
                for widget in container.winfo_children():
                    widget.destroy()
            except Exception as e:
                print(f"❌ {screen_name} — ERROR: {e}")
                traceback.print_exc()
                all_ok = False
        
        root.destroy()
        return all_ok
        
    except Exception as e:
        print(f"❌ Error en validación de pantallas: {e}")
        traceback.print_exc()
        return False


def test_navigation():
    """Prueba que la navegación funcione."""
    print("\n" + "=" * 60)
    print("🧭 VALIDACIÓN DE NAVEGACIÓN")
    print("=" * 60)
    
    try:
        import tkinter as tk
        from app.core.router import Router
        from app.modules.menu import MenuScreen
        from app.modules.union_sheets import UnionSheetsScreen
        
        root = tk.Tk()
        root.withdraw()
        
        container = tk.Frame(root)
        container.pack(fill="both", expand=True)
        
        router = Router(container)
        
        # Test: Navegar a MenuScreen
        router.navigate(MenuScreen)
        print("✅ Navegación a MenuScreen — OK")
        
        # Test: Navegar a UnionSheetsScreen
        router.navigate(UnionSheetsScreen)
        print("✅ Navegación a UnionSheetsScreen — OK")
        
        # Test: Volver a MenuScreen
        router.navigate(MenuScreen)
        print("✅ Volver a MenuScreen — OK")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Error en validación de navegación: {e}")
        traceback.print_exc()
        return False


def main():
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " VALIDADOR DE APLICACIÓN - FastEditable v2.0 ".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    
    results = {
        "Importaciones": test_imports(),
        "Pantallas": test_screen_instantiation(),
        "Navegación": test_navigation(),
    }
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VALIDACIÓN")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name:.<40} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ¡TODAS LAS VALIDACIONES PASARON!")
        print("   La aplicación está lista para usar.")
    else:
        print("❌ ALGUNAS VALIDACIONES FALLARON")
        print("   Revisa los errores arriba.")
    print("=" * 60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
