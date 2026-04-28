# 📊 MAPEO DEL PROGRAMA — FastEditable v2.0

## 📋 Índice
1. [Visión General](#visión-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Estructura de Carpetas](#estructura-de-carpetas)
4. [Flujo de Navegación](#flujo-de-navegación)
5. [Módulos Principales](#módulos-principales)
6. [Sistema de UI](#sistema-de-ui)
7. [Flujo de Datos](#flujo-de-datos)
8. [Stack Tecnológico](#stack-tecnológico)

---

## 🎯 Visión General

**FastEditable** es una herramienta de escritorio basada en Tkinter para procesar y manipular archivos Excel/CSV de forma rápida e intuitiva.

**Objetivo:** Proporcionar 4 operaciones principales para gestionar datos tabulares:
- Unir múltiples hojas dentro de archivos
- Consolidar múltiples archivos en uno
- Separar hojas de un Excel en archivos individuales
- Filtrar, ordenar y seleccionar columnas

**Versión:** 2.0  
**Línea de ejecución:** `python main.py`  
**Resolución mínima:** 860×600 px  
**Tamaño de ventana:** 1100×780 px

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────┐
│         FastEditableApp (main.py)                   │
│  • Inicializa la ventana Tkinter                    │
│  • Crea un Router y la pantalla inicial             │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│         Router (app/core/router.py)                 │
│  • Gestiona navegación entre pantallas              │
│  • Mantiene un contenedor raíz (container)          │
│  • Realiza limpiezas al cambiar de pantalla         │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────┴──────────────┬──────────────┬──────────────┐
         │                          │              │              │
         ▼                          ▼              ▼              ▼
   ┌─────────────┐        ┌──────────────┐  ┌────────────────┐  ┌──────────────┐
   │MenuScreen   │        │UnionSheets   │  │MergeFiles      │  │SplitSheets   │
   └─────────────┘        └──────────────┘  │                │  │              │
         ▲                       ▲            └────────────────┘  └──────────────┘
         │                       │                     ▲
         └───────────────────────┴─────────────────────┘ FilterScreen
                                                      (hereda BaseScreen)


🔄 FLUJO DE NAVEGACIÓN:
   MenuScreen → [1/2/3/4] → Módulo específico → [Volver] → MenuScreen
```

---

## 📁 Estructura de Carpetas

```
FastEditable_v2/
│
├── main.py                          # ⭐ Punto de entrada principal
├── README.md                        # Documentación básica
├── MAPEO_PROGRAMA.md               # Este archivo
│
└── app/                            # Paquete principal
    │
    ├── __init__.py
    │
    ├── core/                       # 🔧 Núcleo del sistema
    │   ├── __init__.py
    │   ├── config.py               # Constantes globales (títulos, dimensiones)
    │   └── router.py               # Sistema de navegación entre pantallas
    │
    ├── ui/                         # 🎨 Sistema de interfaz visual
    │   ├── __init__.py
    │   ├── styles.py               # Paleta de colores, fuentes, dimensiones
    │   ├── components.py           # Widgets reutilizables (botones, tarjetas, etc.)
    │   └── layouts.py              # BaseScreen: plantilla para todas las pantallas
    │
    └── modules/                    # 📦 Módulos funcionales (herencia de BaseScreen)
        ├── __init__.py
        ├── menu.py                 # 🏠 Pantalla principal con 4 opciones
        ├── union_sheets.py         # Módulo 1: Unir hojas
        ├── merge_files.py          # Módulo 2: Unir archivos
        ├── split_sheets.py         # Módulo 3: Separar sheets
        └── filter_module.py        # Módulo 4: Filtrar & Ordenar
```

---

## 🔄 Flujo de Navegación

```
┌──────────────────┐
│   INICIO         │
│   main.py        │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────┐
│   FastEditableApp.__init__()  │
│   • Crea Tkinter root         │
│   • Crea Router               │
│   • navigate(MenuScreen)      │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│          MenuScreen                      │
│   Muestra 4 tarjetas clicables          │
│                                          │
│   [1] UNIR SHEETS                       │
│   [2] UNIR ARCHIVOS                     │
│   [3] SEPARAR SHEETS                    │
│   [4] FILTRAR & ORDENAR                 │
└──┬──────────────────────────────┬────┬──┬┘
   │                              │    │  └─────→ FilterScreen
   │                              │    └──────→ SplitSheetsScreen
   │                              └──────────→ MergeFilesScreen
   └──────────────────────────────────────→ UnionSheetsScreen
           (Cada módulo hereda de BaseScreen)
                         │
                         ▼
            ┌─────────────────────────┐
            │  [← VOLVER]  Título     │
            │  ─────────────────────  │
            │      CONTENIDO          │
            │     (build_body)        │
            │  ─────────────────────  │
            │   [Status bar]          │
            └─────────┬───────────────┘
                      │
                      ▼
              Router.navigate(MenuScreen)
                      │
                      ▼
                  MenuScreen
```

---

## 📦 Módulos Principales

### 1️⃣ **MenuScreen** — Pantalla Principal
**Archivo:** `app/modules/menu.py`

**Función:**
- Presenta la interfaz inicial del programa
- 4 tarjetas interactivas para seleccionar módulo
- No hereda de `BaseScreen` (diseño personalizado)

**Estructura visual:**
```
┌─────────────────────────────────┐
│         [esan | MEDICIONES]     │  ← Header marca
├─────────────────────────────────┤
│ Selecciona una herramienta...   │  ← Subtítulo
├─────────────────────────────────┤
│  ┌──────────────┐ ┌──────────┐  │
│  │ 1            │ │ 2        │  │  ← Grid 2×2
│  │ UNIR SHEETS  │ │ UNIR     │  │
│  │ Procesamiento│ │ ARCHIVOS │  │
│  └──────────────┘ └──────────┘  │
│  ┌──────────────┐ ┌──────────┐  │
│  │ 3            │ │ 4        │  │
│  │ SEPARAR      │ │ FILTRAR  │  │
│  │ SHEETS       │ │ & ORDENAR│  │
│  └──────────────┘ └──────────┘  │
├─────────────────────────────────┤
│    FastEditable v2.0            │  ← Pie
└─────────────────────────────────┘
```

**Atributos:**
- `ITEMS` → Lista de 4 módulos con (número, título, descripción, ruta)
- `_navigate()` → Mapeo dinámico ruta → clase Screen

---

### 2️⃣ **UnionSheetsScreen** — Unir Sheets
**Archivo:** `app/modules/union_sheets.py`

**Función:**
Procesar múltiples archivos Excel, seleccionando hojas específicas de cada uno y consolidarlas.

**Flujo:**
1. Cargar múltiples archivos Excel/CSV
2. Seleccionar hojas a incluir de cada archivo
3. Especificar nombre del archivo de salida
4. Consolidar y guardar resultado

**UI:**
```
┌────────────────────────────────────────────┐
│ ← VOLVER   UNIR SHEETS                     │
├────────────────────────────────────────────┤
│ [+ Cargar archivos]  [Consolidar y guardar]│
├────────────────────────────────────────────┤
│  ┌──────────────┐ ┌─────────────────────┐  │
│  │ ARCHIVOS     │ │ CONFIGURACIÓN SALIDA│  │
│  │ CARGADOS     │ │ • Nombre archivo    │  │
│  │              │ │   [entrada texto]   │  │
│  │ • archivo1   │ │ • Hojas a incluir:  │  │
│  │ • archivo2   │ │   ☑ Hoja1          │  │
│  │ • archivo3   │ │   ☑ Hoja2          │  │
│  └──────────────┘ │   ☑ Hoja3          │  │
│                   └─────────────────────┘  │
├────────────────────────────────────────────┤
│ Status: Listo                              │
└────────────────────────────────────────────┘
```

**Datos internos:**
- `batch_files: dict` → `{ruta: {sheets: dict, vars: {}, out_name: str}}`
- `_sel_path: str|None` → Archivo seleccionado actualmente

---

### 3️⃣ **MergeFilesScreen** — Unir Archivos
**Archivo:** `app/modules/merge_files.py`

**Función:**
Consolidar múltiples archivos Excel/CSV en un único archivo.

**Flujo:**
1. Seleccionar N archivos Excel/CSV
2. Concatenar todos los DataFrames (incluyendo todas las hojas de cada Excel)
3. Guardar resultado consolidado

**UI:**
```
┌────────────────────────────────────────────┐
│ ← VOLVER   UNIR ARCHIVOS                   │
├────────────────────────────────────────────┤
│ [+ Seleccionar archivos] [Consolidar y ...]│
├────────────────────────────────────────────┤
│ Archivos seleccionados:                    │
│ ┌──────────────────────────────────────┐   │
│ │  ✓  archivo1.xlsx                    │   │
│ │  ✓  archivo2.csv                     │   │
│ │  ✓  archivo3.xlsx                    │   │
│ └──────────────────────────────────────┘   │
│ [3 archivo(s) seleccionado(s)]             │
├────────────────────────────────────────────┤
│ Status: 3 archivo(s) listos para consolidar
└────────────────────────────────────────────┘
```

**Datos internos:**
- `_files: list[str]` → Lista de rutas de archivo

---

### 4️⃣ **SplitSheetsScreen** — Separar Sheets
**Archivo:** `app/modules/split_sheets.py`

**Función:**
Dividir un archivo Excel en múltiples archivos, uno por hoja.

**Flujo:**
1. Abrir un archivo Excel
2. Seleccionar hojas a exportar
3. Elegir carpeta de destino
4. Guardar cada hoja en un archivo separado

**UI:**
```
┌────────────────────────────────────────────┐
│ ← VOLVER   SEPARAR SHEETS                  │
├────────────────────────────────────────────┤
│ [Abrir archivo Excel]  [Separar y guardar] │
├────────────────────────────────────────────┤
│ Hojas encontradas:                         │
│ ┌──────────────────────────────────────┐   │
│ │ ☑ Hoja1                   100 filas │   │
│ │ ☑ Hoja2                    250 filas │   │
│ │ ☑ Configuración             50 filas │   │
│ └──────────────────────────────────────┘   │
│ [3 hoja(s) disponibles]                    │
├────────────────────────────────────────────┤
│ Status: Archivo cargado: 3 hoja(s)         │
└────────────────────────────────────────────┘
```

**Datos internos:**
- `_df_dict: dict` → `{nombre_hoja: DataFrame}`
- `_sheet_vars: dict` → `{nombre_hoja: BooleanVar}`

---

### 5️⃣ **FilterScreen** — Filtrar & Ordenar
**Archivo:** `app/modules/filter_module.py`

**Función:**
Aplicar filtros inteligentes, ordenamientos múltiples y seleccionar columnas.

**Características avanzadas:**
- 🔤 **Filtros por tipo de dato:**
  - Texto → Checkboxes con búsqueda
  - Numérico → Rango min/max
  - Fecha → Rango de fechas
- 📊 **Ordenamiento múltiple** con drag-drop
- 📋 **Selección de columnas** con vista previa
- 🎯 **Validación y feedback en tiempo real**

**Flujo:**
1. Cargar archivo CSV/Excel
2. Detectar tipo de cada columna
3. Configurar filtros por columna
4. Ordenar por múltiples criterios
5. Seleccionar columnas
6. Vista previa en vivo
7. Aplicar y guardar

**Helpers clave:**
- `_col_kind()` → Detecta si columna es "numeric", "datetime" o "text"
- `ColumnFilterPanel` → Panel colapsable para filtrar una columna

---

## 🎨 Sistema de UI

### 1. **styles.py** — Paleta y Tipografía
```python
# Colores
C_RED      = "#E31937"   (Rojo principal - acciones)
C_DARK     = "#1C1C1E"   (Gris oscuro - headers)
C_BG       = "#F2F3F5"   (Gris claro - fondo)
C_BG_CARD  = "#FFFFFF"   (Blanco - tarjetas)

# Estados
C_SUCCESS  = "#1A7F4B"   (Verde)
C_WARN     = "#D97706"   (Naranja)
C_INFO     = "#1D6FBF"   (Azul)

# Fuentes
F_BRAND    = Georgia 38b (Logo marca)
F_H1       = Segoe UI 18b (Títulos principales)
F_BTN      = Segoe UI 11b (Botones)
F_BODY     = Segoe UI 10 (Texto general)
```

### 2. **components.py** — Widgets Reutilizables

**Botones:**
- `PrimaryBtn` → Fondo rojo, acción principal
- `SecondaryBtn` → Borde, acciones secundarias
- `GhostBtn` → Transparente, acciones menores
- `BackBtn` → Especial para retroceder
- `IconBtn` → Pequeño, solo símbolo

**Etiquetas:**
- `H1`, `H2` → Títulos
- `BodyLabel` → Texto general
- `Badge` → Etiquetas coloreadas (success/warn/info/red)

**Contenedores:**
- `Card` → Frame con fondo blanco y borde
- `ScrollableFrame` → Frame con scrollbar vertical
- `Divider` → Línea horizontal

**Otros:**
- `StatusBar` → Barra de estado inferior

---

### 3. **layouts.py** — Plantilla Base

**BaseScreen** — Clase abstracta que todas las pantallas heredan:

```
┌─────────────────────────────┐
│ top_bar                     │  (← VOLVER   Título   [Toolbar])
│ ─────────────────────────── │
│                             │
│ body                        │  (fill/expand)
│ (subclase implementa aquí)  │
│                             │
│ ─────────────────────────── │
│ status_bar                  │
└─────────────────────────────┘
```

**Flujo de herencia:**
```
BaseScreen (plantilla)
    ├── UnionSheetsScreen (build_body override)
    ├── MergeFilesScreen
    ├── SplitSheetsScreen
    └── FilterScreen
```

---

## 📊 Flujo de Datos

### Ciclo típico (ejemplo: UnionSheets)

```
┌─────────────────────┐
│  Haz clic en tarjeta│ (MenuScreen)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│ Router.navigate(             │
│   UnionSheetsScreen)        │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ UnionSheetsScreen.render()  │
│ → _build_shell (BaseScreen) │
│ → build_body (override)     │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Cargar archivos             │
│ filedialog.askopenfilenames │
│ ↓                           │
│ batch_files = {             │
│   ruta: {                   │
│     'sheets': pd.read_excel │
│     'vars': BooleanVars     │
│   }                         │
│ }                           │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Procesar                    │
│ pd.concat(hojas_selec)      │
│ ↓                           │
│ df.to_excel(path)           │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ messagebox.showinfo         │
│ "Guardado correctamente"    │
└─────────────────────────────┘
```

### Stack de librerías de datos:
```
pandas          → Lectura/escritura Excel/CSV
tkinter.filedialog → Diálogos de archivos
tkinter.messagebox → Alertas/confirmaciones
```

---

## 🔧 Stack Tecnológico

| Capa | Tecnología | Función |
|------|-----------|---------|
| **Framework UI** | Tkinter | Interfaz gráfica de escritorio |
| **Procesamiento** | Pandas | Lectura/escritura de datos, transformación |
| **Diálogos** | tkinter.filedialog | Selección de archivos/carpetas |
| **Lenguaje** | Python 3.12+ | Lógica principal |
| **Gestión de estado** | tkinter Variables | Control de widgets |

---

## 🎯 Puntos de entrada clave

**`main.py`** → `FastEditableApp()`
- Inicializa ventana Tkinter
- Crea Router
- Navega a MenuScreen

**`app/core/router.py`** → `Router.navigate(screen_class)`
- Limpia contenedor actual
- Instancia nueva pantalla
- Llama a `render()`

**`app/core/config.py`** → Constantes globales
- Títulos, dimensiones, versión

**`app/ui/layouts.py`** → `BaseScreen.render()`
- Construye estructura fija (header, body, footer)
- Llama a `build_body()` para que subclases personalicen

---

## 📝 Convenciones de código

### Naming
- Clases con CamelCase: `UnionSheetsScreen`
- Métodos privados con `_`: `_load_files()`
- Constantes en MAYUSCULAS: `C_RED`, `APP_TITLE`

### Estructura de clases
```python
class MyScreen(BaseScreen):
    title = "TÍTULO"
    
    def __init__(self, container, router):
        super().__init__(container, router)
        # Estado específico
    
    def build_body(self, parent):
        # Construir interfaz
        pass
    
    def _load(self):
        # Métodos privados
        pass
```

### Imports
```python
from app.ui import styles as s          # Alias universal
from app.ui.components import PrimaryBtn
from app.ui.layouts import BaseScreen
```

---

## 🚀 Cómo agregar un nuevo módulo

1. **Crear archivo** en `app/modules/nuevo_modulo.py`
2. **Crear clase** que herede de `BaseScreen`
3. **Implementar** `build_body(self, parent)` y métodos privados
4. **Agregar entrada** en `MenuScreen.ITEMS`
5. **Registrar ruta** en `MenuScreen._navigate()` MAP

Ejemplo:
```python
# app/modules/nuevo_modulo.py
from app.ui.layouts import BaseScreen

class NuevoScreen(BaseScreen):
    title = "MI NUEVO MÓDULO"
    
    def __init__(self, container, router):
        super().__init__(container, router)
    
    def build_body(self, parent):
        # Tu código aquí
        pass
```

---

## 📚 Resumen de archivos clave

| Archivo | Líneas | Función |
|---------|--------|---------|
| `main.py` | ~25 | Punto de entrada, inicialización |
| `app/core/config.py` | ~5 | Constantes globales |
| `app/core/router.py` | ~20 | Sistema de navegación |
| `app/ui/styles.py` | ~40 | Paleta y tipografía |
| `app/ui/components.py` | ~200+ | Widgets reutilizables |
| `app/ui/layouts.py` | ~60 | Plantilla BaseScreen |
| `app/modules/menu.py` | ~100+ | Pantalla principal |
| `app/modules/union_sheets.py` | ~150+ | Módulo unir sheets |
| `app/modules/merge_files.py` | ~80+ | Módulo unir archivos |
| `app/modules/split_sheets.py` | ~100+ | Módulo separar sheets |
| `app/modules/filter_module.py` | ~300+ | Módulo filtrar & ordenar |

---

## 🎓 Diagrama de dependencias

```
main.py
   ↓
FastEditableApp
   ↓
Router ← ← ← ← ← ← ← ← → [config.py]
   ↓
   ├─→ MenuScreen
   │      ↓
   │   components.py (Divider, Card)
   │   styles.py
   │
   ├─→ UnionSheetsScreen
   │      ↓
   │   BaseScreen ← layouts.py
   │      ↓
   │   components.py (PrimaryBtn, SecondaryBtn, etc.)
   │   styles.py
   │   pandas
   │
   ├─→ MergeFilesScreen
   │      ↓ (idem)
   │
   ├─→ SplitSheetsScreen
   │      ↓ (idem)
   │
   └─→ FilterScreen
          ↓ (idem + componentes avanzados)
```

---

## 📌 Próximos pasos sugeridos

- [ ] Agregar persistencia (guardar preferencias)
- [ ] Crear testing unitario para pandas operations
- [ ] Internacionalización (ES/EN/etc.)
- [ ] Historial de operaciones recientes
- [ ] Drag-drop de archivos en interfaz
- [ ] Cancelación asíncrona de operaciones largas

---

**Última actualización:** 21 abril 2026  
**Autor:** FastEditable Team  
**Estado:** Documentación v1.0
