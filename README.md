# FastEditable — MEDICIONES
## Estructura del Proyecto

```
FastEditable/
├── main.py                  # Punto de entrada
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Constantes y configuración global
│   │   └── router.py        # Navegación entre pantallas
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── styles.py        # Paleta, fuentes, temas
│   │   ├── components.py    # Widgets reutilizables (botones, cards, etc.)
│   │   └── layouts.py       # Marcos base reutilizables
│   └── modules/
│       ├── __init__.py
│       ├── menu.py          # Pantalla principal / menú
│       ├── union_sheets.py  # Módulo: Unir Sheets
│       ├── merge_files.py   # Módulo: Unir Archivos
│       ├── split_sheets.py  # Módulo: Separar Sheets
│       └── filter_module.py # Módulo: Filtrar (mejorado)
├── assets/
│   └── (íconos, fuentes opcionales)
└── README.md
```
