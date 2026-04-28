"""
Script maestro de pruebas — Ejecuta todas las validaciones en orden.
"""

import subprocess
import sys
import os


def run_command(cmd, description):
    """Ejecuta un comando y muestra el resultado."""
    print("\n" + "=" * 70)
    print(f"🔄 {description}")
    print("=" * 70)
    
    result = subprocess.run(cmd, shell=True, cwd=os.path.dirname(__file__) or ".")
    return result.returncode == 0


def main():
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " SUITE DE PRUEBAS COMPLETA - FastEditable v2.0 ".center(68) + "║")
    print("╚" + "=" * 68 + "╝")

    # Cambiar a directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    results = {}

    # 1. Validar importaciones y estructura
    results["validate.py"] = run_command(
        f"{sys.executable} validate.py",
        "Ejecutando validación de estructura"
    )

    # 2. Pruebas automáticas de navegación
    results["test_auto.py"] = run_command(
        f"{sys.executable} test_auto.py",
        "Ejecutando pruebas automáticas de navegación"
    )

    # Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 70)

    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        print(f"{test_name:.<50} {status}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        print("\n   Tu aplicación FastEditable está completamente funcional.")
        print("   Los botones del menú ahora responden correctamente.")
        print("\n   Puedes ejecutar: python main.py")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
        print("   Revisa los errores arriba para más detalles.")
    print("=" * 70 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
