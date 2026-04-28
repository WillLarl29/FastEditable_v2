# 🎯 REFERENCIA RÁPIDA — FastEditable v2.0

## 📑 Tabla de Contenidos Rápida

### Archivos Principales

| Archivo | Propósito | Líneas |
|---------|-----------|--------|
| `main.py` | Punto de entrada | ~25 |
| `app/core/config.py` | Constantes globales | ~5 |
| `app/core/router.py` | Sistema de navegación | ~20 |
| `app/ui/styles.py` | Colores, fuentes | ~45 |
| `app/ui/components.py` | Widgets | ~250 |
| `app/ui/layouts.py` | Plantilla BaseScreen | ~65 |
| `app/modules/menu.py` | Menú principal | ~120 |
| `app/modules/union_sheets.py` | Unir hojas | ~200 |
| `app/modules/merge_files.py` | Unir archivos | ~100 |
| `app/modules/split_sheets.py` | Separar hojas | ~120 |
| `app/modules/filter_module.py` | Filtrar datos | ~400 |

---

## 🚀 Cómo ejecutar

```bash
cd FastEditable_v2
python main.py
```

---

## 🎨 Paleta de Colores Completa

```python
# Primarios
C_RED      = "#E31937"  # Rojo principal (botones, enlaces)
C_RED_DK   = "#B5122B"  # Rojo oscuro (hover)
C_RED_LT   = "#FDEAED"  # Rojo claro (selección)

# Neutrales
C_DARK     = "#1C1C1E"  # Negro (headers)
C_GRAY     = "#53565A"  # Gris (texto principal)
C_GRAY_LT  = "#8A8D91"  # Gris claro (helper text)
C_BORDER   = "#DDDFE2"  # Gris borde
C_BG       = "#F2F3F5"  # Fondo gris muy claro
C_BG_CARD  = "#FFFFFF"  # Fondo tarjeta
C_WHITE    = "#FFFFFF"  # Blanco puro

# Estados
C_SUCCESS  = "#1A7F4B"  # Verde
C_WARN     = "#D97706"  # Naranja
C_INFO     = "#1D6FBF"  # Azul
```

---

## 🔤 Tipografía

```python
F_BRAND    = ("Georgia", 38, "bold")     # Logo
F_SUBBRAND = ("Georgia", 22)             # Subtítulo marca
F_H1       = ("Segoe UI", 18, "bold")    # Título página
F_H2       = ("Segoe UI", 13, "bold")    # Subtítulo
F_BODY     = ("Segoe UI", 10)            # Texto normal
F_SMALL    = ("Segoe UI", 9)             # Texto pequeño
F_MONO     = ("Consolas", 9)             # Monospace
F_BTN      = ("Segoe UI", 11, "bold")    # Botones grandes
F_BTN_SM   = ("Segoe UI", 9, "bold")     # Botones pequeños
```

---

## 🔘 Componentes Disponibles

### Botones

```python
# Botón primario (rojo, para acciones principales)
PrimaryBtn(parent, "Guardar", command=on_save)

# Botón secundario (borde, acciones secundarias)
SecondaryBtn(parent, "Cancelar", command=on_cancel)

# Botón fantasma (sin borde, acciones menores)
GhostBtn(parent, "Más opciones", command=on_more)

# Botón volver
BackBtn(parent, command=lambda: router.navigate(MenuScreen))

# Botón ícono (pequeño, solo símbolo)
IconBtn(parent, "×", command=on_delete)
```

### Etiquetas

```python
# Títulos
H1(parent, "Título principal")
H2(parent, "Subtítulo")

# Texto normal
BodyLabel(parent, "Texto descriptivo")

# Chips/badges coloreados
Badge(parent, "Éxito", kind="success")    # Verde
Badge(parent, "Advertencia", kind="warn")  # Naranja
Badge(parent, "Info", kind="info")        # Azul
Badge(parent, "Rojo", kind="red")         # Rojo
```

### Contenedores

```python
# Card: frame blanco con borde sutil
card = Card(parent, padx=14, pady=14)

# Divider: línea horizontal
Divider(parent)

# ScrollableFrame: frame con scrollbar vertical
scrollable = ScrollableFrame(parent, height=200)
label = tk.Label(scrollable.inner, text="Contenido")
label.pack()

# StatusBar: barra de estado
status = StatusBar(parent)
status.set("Mensaje", "Info extra")
```

---

## 📱 Estructura de Pantalla Base

Todas las pantallas (excepto MenuScreen) heredan de `BaseScreen`:

```python
class MiScreen(BaseScreen):
    title = "MI TÍTULO"
    
    def __init__(self, container, router):
        super().__init__(container, router)
        self._estado = {}
    
    def build_body(self, parent):
        # Aquí va tu contenido
        tk.Label(parent, text="Hola").pack()
```

**Estructura automática:**
```
┌────────────────────────────┐
│ ← VOLVER   [MI TÍTULO]     │  ← self.top_bar (automático)
├────────────────────────────┤
│                            │
│  Tu contenido aquí         │  ← self.body (fill/expand)
│  (build_body())            │
│                            │
├────────────────────────────┤
│ Listo                      │  ← self.status (automático)
└────────────────────────────┘
```

---

## 🧭 Navegación

```python
# En MenuScreen → Navegar a UnionSheetsScreen
self.router.navigate(UnionSheetsScreen)

# Con parámetros
self.router.navigate(UnionSheetsScreen, preset_file="data.xlsx")

# En qualquier pantalla → Volver a MenuScreen
self.router.navigate(MenuScreen)
```

---

## 📊 Operaciones Pandas Comunes

### Leer datos

```python
# Excel
df = pd.read_excel("archivo.xlsx")
all_sheets = pd.read_excel("archivo.xlsx", sheet_name=None)

# CSV
df = pd.read_csv("archivo.csv")
```

### Manipular datos

```python
# Filtrar filas
df_filtered = df[df["columna"] > 100]

# Seleccionar columnas
df_selected = df[["col1", "col2", "col3"]]

# Ordenar
df_sorted = df.sort_values(by=["col1"], ascending=True)

# Concatenar
df_combined = pd.concat([df1, df2, df3], ignore_index=True)
```

### Guardar datos

```python
# Excel
df.to_excel("output.xlsx", index=False)

# CSV
df.to_csv("output.csv", index=False)
```

---

## 🎯 Patrones Comunes

### Patrón 1: Cargar Archivos

```python
def _load_files(self):
    paths = filedialog.askopenfilenames(
        filetypes=[("Excel/CSV", "*.xlsx *.csv")])
    
    for path in paths:
        # Procesar
        if path.endswith(".csv"):
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)
        # Guardar en estado
        self._files.append(path)
    
    self.status.set(f"{len(self._files)} archivo(s) cargado(s)")
```

### Patrón 2: Mostrar Mensaje

```python
def _run(self):
    try:
        # Procesar
        result = hacer_algo()
        messagebox.showinfo("Éxito", f"Listo: {result}")
        self.status.set("Operación completada")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        self.status.set("Error")
```

### Patrón 3: Widget Dinámico

```python
def _refresh_list(self):
    # Limpiar
    for widget in self._container.winfo_children():
        widget.destroy()
    
    # Recrear
    for item in self._items:
        row = tk.Frame(self._container)
        row.pack(fill="x", padx=10, pady=4)
        tk.Label(row, text=item).pack(side="left")
```

### Patrón 4: Control de Estado

```python
def _update_status(self):
    if self._items:
        self._btn_process.config(state="normal")
        self.status.set(f"{len(self._items)} elemento(s) listos")
    else:
        self._btn_process.config(state="disabled")
        self.status.set("Carga archivos para continuar")
```

---

## 🐛 Debug

### Ver qué módulos importados hay

```python
import sys
print([m for m in sys.modules.keys() if 'app' in m])
```

### Log simple

```python
# Agregar a cualquier lado
print(f"DEBUG: {variable}")
self.status.set(f"DEBUG: {value}")
```

### Inspeccionar DataFrame

```python
# En una pantalla
print(df.head())
print(df.info())
print(df.describe())
```

---

## ✅ Checklist: Crear Nuevo Módulo

- [ ] Crear `app/modules/mi_modulo.py`
- [ ] Heredar de `BaseScreen`
- [ ] Definir `title = "MI MÓDULO"`
- [ ] Implementar `build_body(self, parent)`
- [ ] Agregar a `MenuScreen.ITEMS`
- [ ] Importar en `MenuScreen._navigate()`
- [ ] Registrar en MAP dict
- [ ] Probar: `python main.py` → clic opción → navega bien → volver funciona

---

## 🎓 Imports Típicos

```python
# UI
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# App
from app.ui import styles as s
from app.ui.components import PrimaryBtn, SecondaryBtn, Card
from app.ui.layouts import BaseScreen

# Datos
import pandas as pd
import os
```

---

## 💾 Variables Comunes

```python
# tk.BooleanVar() → Checkbox
var = tk.BooleanVar(value=True)
var.get()  # Obtener valor
var.set(False)  # Cambiar valor

# tk.StringVar() → Entry
text_var = tk.StringVar()
text_var.trace_add("write", callback)  # Reaccionar a cambios

# Diktorios para estado
self._data = {
    "ruta": {"sheets": {}, "vars": {}}
}
```

---

## 📏 Dimensiones Estándar

```python
# Ventana principal
APP_WIDTH  = 1100
APP_HEIGHT = 780
MIN_WIDTH  = 860
MIN_HEIGHT = 600

# Padding
PAD_LG = 24  # Grande
PAD_MD = 14  # Medio
PAD_SM = 8   # Pequeño

# Borde simulado
RADIUS = 6
```

---

## 🔗 Flujo Rápido de cualquier Operación

1. **Usuario hace clic**
2. **Método privado se ejecuta** (`_load_files`, `_process`, etc)
3. **Cargar datos** (`filedialog`, `pd.read_*`)
4. **Validar**
5. **Procesar** (pandas operations)
6. **Guardar** (`df.to_*`, `filedialog.asksaveasfilename`)
7. **Feedback** (`messagebox`, `self.status.set`)

---

## 🎨 Tema Visual Resumido

- **Logo/Marca**: Georgia 38b, rojo (#E31937)
- **Títulos**: Segoe UI 18b, gris oscuro (#1C1C1E)
- **Texto**: Segoe UI 10, gris (#53565A)
- **Botones**: Fondo rojo, hover oscuro
- **Tarjetas**: Fondo blanco, borde gris claro
- **Selección**: Rojo claro (#FDEAED)
- **Estados**: Verde (éxito), Naranja (alerta), Azul (info)

---

## 📞 Contactos Internos

- **Config global**: `app/core/config.py`
- **Cambiar estilos**: `app/ui/styles.py`
- **Agregar widgets**: `app/ui/components.py`
- **Cambiar estructura base**: `app/ui/layouts.py`
- **Nueva pantalla**: `app/modules/nuevo.py` + registrar en menu

---

## 🆘 Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ModuleNotFoundError: pandas` | Pandas no instalado | `pip install pandas` |
| `Tkinter no aparece` | Problema de ventana | Reiniciar terminal |
| Widget no aparece | No llamó `.pack()` o `.grid()` | Agregar layout manager |
| Botón sin efecto | `command` incorrecto | Verificar referencia función |
| Status bar no actualiza | Olvidó `self.status.set()` | Llamar método |
| Listbox vacío | Olvidó `.insert()` o `.pack()` | Verificar código |
| Archivo no encontrado | Ruta relativa incorrecta | Usar `filedialog` |

---

## 🚀 Tips de Rendimiento

- Usar `pd.read_excel(..., sheet_name=None)` para múltiples hojas
- No recrear widgets innecesariamente (actualizar con `.config()`)
- Para listas grandes, usar `Listbox` con scrollbar
- `pd.concat()` es más rápido que append en loop
- `ignore_index=True` cuando concatenas

---

**Última actualización:** 21 abril 2026  
**Versión:** 1.0
