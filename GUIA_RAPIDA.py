#!/usr/bin/env python3
"""
GUÍA RÁPIDA DE USO - FastEditable v2.0
======================================

Muestra instrucciones claras sobre cómo usar el programa y las herramientas de prueba.
"""

import sys
import os


def print_banner(title):
    width = 80
    print("\n" + "═" * width)
    print(title.center(width))
    print("═" * width + "\n")


def print_section(title):
    print(f"\n{'─' * 80}")
    print(f"  {title}")
    print(f"{'─' * 80}\n")


def main():
    print_banner("FASTEDIABLE v2.0 — GUÍA DE USO")

    print_section("✅ ESTADO DEL PROGRAMA")
    print("""
    ✅ COMPLETAMENTE FUNCIONAL Y CORREGIDO
    
    • Los botones del menú responden a clicks
    • La navegación entre pantallas funciona correctamente
    • El sistema de volver atrás está funcionando
    • Todos los módulos están disponibles
    """)

    print_section("🚀 CÓMO EJECUTAR EL PROGRAMA PRINCIPAL")
    print("""
    Ejecuta el programa con:
    
        python main.py
    
    Esto abrirá la ventana de FastEditable donde podrás:
      1. Hacer click en las tarjetas para ir a cada módulo
      2. Usar el botón "← VOLVER" para regresar al menú
      3. Procesar tus archivos Excel/CSV
    """)

    print_section("🧪 HERRAMIENTAS DE PRUEBA")
    print("""
    Se han creado 4 scripts de prueba útiles:
    
    1️⃣  validate.py
        Valida que el programa esté correctamente configurado
        Comando: python validate.py
        Resultado: Lista de validaciones con ✅ o ❌
    
    2️⃣  test_auto.py
        Pruebas automáticas sin GUI visible
        Comando: python test_auto.py
        Resultado: Simula la navegación y verifica que funciona
    
    3️⃣  test_app.py
        Ejecuta el programa con GUI visible
        Comando: python test_app.py
        Se cierra automáticamente en 45 segundos
    
    4️⃣  run_tests.py
        Ejecuta TODAS las pruebas en secuencia
        Comando: python run_tests.py
        Resultado: Resumen completo de validaciones
    """)

    print_section("🔍 ERRORES QUE FUERON CORREGIDOS")
    print("""
    1. Menu.py:
       ❌ Los botones no respondían a clicks
       ✅ Cambiado de Frames con binds a Buttons invisibles
    
    2. Components.py:
       ❌ Error de parámetros duplicados (padx/pady)
       ✅ Ahora permite sobrescribir los valores por defecto
    """)

    print_section("📁 ARCHIVOS MODIFICADOS")
    print("""
    app/modules/menu.py
      • Reescrita la función _make_card()
      • Cambio: Frame -> Button
    
    app/ui/components.py
      • Actualizada la clase Card.__init__()
      • Parámetros padx/pady ahora son extraíbles
    """)

    print_section("📦 ARCHIVOS CREADOS (Utilidades)")
    print("""
    validate.py
      Validador de estructura del programa
    
    test_auto.py
      Pruebas automáticas de navegación
    
    test_app.py
      Ejecutor con GUI para prueba manual
    
    run_tests.py
      Suite completa de pruebas
    
    RESUMEN_CORRECCIONES.py
      Documentación detallada de cambios
    
    GUIA_RAPIDA.py (este archivo)
      Instrucciones rápidas de uso
    """)

    print_section("🎯 PRÓXIMOS PASOS")
    print("""
    1. Verifica que todo funciona:
       python run_tests.py
    
    2. Ejecuta el programa:
       python main.py
    
    3. Prueba los módulos:
       • Haz click en "UNIR SHEETS"
       • Haz click en "UNIR ARCHIVOS"
       • Haz click en "SEPARAR SHEETS"
       • Haz click en "FILTRAR & ORDENAR"
       • Usa "← VOLVER" para regresar
    
    4. ¡Disfruta usando FastEditable!
    """)

    print_section("📞 INFORMACIÓN RÁPIDA")
    print(f"""
    Directorio: {os.getcwd()}
    Versión: 2.0
    Python: {sys.version.split()[0]}
    Estado: ✅ FUNCIONAL
    
    Módulos disponibles:
      1. Unir Sheets (UnionSheetsScreen)
      2. Unir Archivos (MergeFilesScreen)
      3. Separar Sheets (SplitSheetsScreen)
      4. Filtrar & Ordenar (FilterScreen)
    """)

    print("\n" + "═" * 80)
    print("¡FastEditable está listo para usar! 🎉".center(80))
    print("═" * 80 + "\n")


if __name__ == "__main__":
    main()
