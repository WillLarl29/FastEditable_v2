# 🔬 ANÁLISIS TÉCNICO DETALLADO — FastEditable v2.0

## Tabla de Contenidos
1. [Sistema de Router](#sistema-de-router)
2. [BaseScreen - Arquitectura](#basescreen---arquitectura)
3. [Módulo: Union Sheets](#módulo-union-sheets)
4. [Módulo: Merge Files](#módulo-merge-files)
5. [Módulo: Split Sheets](#módulo-split-sheets)
6. [Módulo: Filter Module](#módulo-filter-module)
7. [Sistema de Estilos](#sistema-de-estilos)
8. [Gestión de Estado](#gestión-de-estado)

---

## Sistema de Router

### Concepto
El `Router` es un gestor de navegación que actúa como controlador central. Mantiene un contenedor Tkinter donde se renderizar las pantallas.

### Código clave
```python
class Router:
    def __init__(self, container):
        self.container = container      # Frame principal de Tkinter
        self._current = None            # Pantalla actual
    
    def _clear(self):
        """Destruye todos los widgets hijos del contenedor."""
        for widget in self.container.winfo_children():
            widget.destroy()
    
    def navigate(self, screen_class, **kwargs):
        """
        Navega a una nueva pantalla:
        1. Limpia widgets anteriores
        2. Instancia la nueva pantalla
        3. Llama render() para construir interfaz
        """
        self._clear()
        self._current = screen_class(self.container, self, **kwargs)
        self._current.render()
```

### Flujo de navegación
```
Router.navigate(UnionSheetsScreen)
    ↓
_clear()  ← Destruye MenuScreen y todos sus widgets
    ↓
UnionSheetsScreen(container, router).__init__()
    ↓
screen.render()  ← Construye nueva interfaz
    ↓
_build_shell()  ← BaseScreen
build_body()    ← UnionSheetsScreen override
    ↓
Pantalla lista para interacción
```

### Ventajas
- ✅ Limpiezas automáticas de memoria
- ✅ Transiciones suaves entre pantallas
- ✅ Reutilización del contenedor
- ✅ Paso fácil de contexto via `**kwargs`

---

## BaseScreen - Arquitectura

### Propósito
Plantilla abstracta que define la estructura fija de todas las pantallas:
- Top bar (botón volver + título)
- Body (contenido personalizado)
- Status bar (feedback)

### Diagrama de estructura

```
┌─────────────────────────────────────┐
│ _build_shell() crea esto:           │
│                                     │
│ top_bar (pack fill="x")             │
│ ├─ BackBtn                          │
│ ├─ Label (title)                    │
│ └─ toolbar (frame para extras)      │
│                                     │
│ Divider (línea)                     │
│                                     │
│ body (pack fill="both", expand=True)│
│ (vacío hasta que build_body rellena)│
│                                     │
│ status (pack fill="x", side="bottom")│
│ └─ StatusBar con mensaje + info     │
└─────────────────────────────────────┘
```

### Código esencial

```python
class BaseScreen:
    title = "Pantalla"
    
    def __init__(self, container, router):
        self.container = container
        self.router = router
    
    def render(self):
        """Template Method: construye shell + llama build_body"""
        self._build_shell()
        self.build_body(self.body)
    
    def _build_shell(self):
        # 1. Top bar
        self.top_bar = tk.Frame(self.container, bg=s.C_BG, pady=8)
        self.top_bar.pack(fill="x", padx=s.PAD_LG)
        
        BackBtn(self.top_bar, 
                command=lambda: self.router.navigate(MenuScreen))
        .pack(side="left")
        
        tk.Label(self.top_bar, text=self.title, 
                 font=s.F_H1, bg=s.C_BG, fg=s.C_DARK)
        .pack(side="left", padx=12)
        
        self.toolbar = tk.Frame(self.top_bar, bg=s.C_BG)
        self.toolbar.pack(side="right")
        
        # 2. Divider
        Divider(self.container).pack(fill="x")
        
        # 3. Body (vacío hasta build_body)
        self.body = tk.Frame(self.container, bg=s.C_BG)
        self.body.pack(fill="both", expand=True)
        
        # 4. Status bar
        self.status = StatusBar(self.container)
        self.status.pack(fill="x", side="bottom")
    
    def build_body(self, parent):
        """Override en subclases"""
        raise NotImplementedError
```

### Pattern de herencia
```python
class MiScreen(BaseScreen):
    title = "MI PANTALLA"
    
    def __init__(self, container, router):
        super().__init__(container, router)
        # Estado específico de esta pantalla
        self._files = []
    
    def build_body(self, parent):
        # Rellenar self.body con widgets
        tk.Label(parent, text="Contenido").pack()
        btn = PrimaryBtn(parent, "Procesar", command=self._process)
        btn.pack()
    
    def _process(self):
        # Lógica privada
        pass
```

### Acceso a elementos desde cualquier método

```python
class MiScreen(BaseScreen):
    def build_body(self, parent):
        self._btn = PrimaryBtn(parent, "Guardar", command=self._save)
        self._btn.pack()
    
    def _save(self):
        # Desde cualquier método puedes acceder a:
        self.status.set("Guardando...")  # Actualizar status
        self._btn.config(state="disabled")  # Deshabilitar botón
        self.router.navigate(MenuScreen)  # Navegar
```

---

## Módulo: Union Sheets

### Propósito
Procesar múltiples archivos Excel seleccionando hojas específicas de cada uno y consolidarlas en un solo archivo.

### Caso de uso
```
Tengo 3 archivos:
  • ventas_enero.xlsx → hojas: [Región A, Región B, Región C]
  • ventas_febrero.xlsx → hojas: [Región A, Región B, Región C]
  • ventas_marzo.xlsx → hojas: [Región A, Región B, Región C]

Quiero:
  • Obtener todas las "Región A" de los 3 archivos
  • Concatenarlas en un solo DF
  • Guardar como "Región_A_Consolidado.xlsx"
```

### Estructura de datos
```python
self.batch_files = {
    "C:/ruta/ventas_enero.xlsx": {
        "sheets": {
            "Región A": DataFrame (100 filas),
            "Región B": DataFrame (150 filas),
            "Región C": DataFrame (120 filas)
        },
        "vars": {
            "Región A": BooleanVar(value=True),
            "Región B": BooleanVar(value=True),
            "Región C": BooleanVar(value=True)
        },
        "out_name": "consolidado_enero"
    },
    "C:/ruta/ventas_febrero.xlsx": {
        # idem
    }
}
```

### Flujo de procesamiento

```
1. _load_files()
   ├─ filedialog.askopenfilenames() → lista de rutas
   ├─ Para cada ruta:
   │  ├─ if .csv: pd.read_csv() → {"CSV": df}
   │  └─ else: pd.read_excel(sheet_name=None) → {hoja: df, ...}
   │
   └─ batch_files[ruta] = {sheets, vars, out_name}

2. _on_select() [cuando usuario selecciona archivo en listbox]
   ├─ Obtiene archivo seleccionado
   ├─ Limpia _sheets_scroll
   └─ Dibuja checkboxes de hojas seleccionables

3. _update_out_name() [cuando user tipea en campo]
   ├─ Actualiza batch_files[sel_path]["out_name"]
   └─ Habilita _btn_process si hay nombre

4. _process()
   ├─ Para cada archivo en batch_files:
   │  ├─ Obtiene hojas seleccionadas
   │  ├─ Concatena: pd.concat(dfs, ignore_index=True)
   │  └─ Guarda resultado en temp
   │
   ├─ Concatena todos los temp
   ├─ filedialog.asksaveasfilename()
   └─ df.to_excel(path, index=False)
```

### Pseudocódigo de _process

```python
def _process(self):
    all_dfs = []
    
    for archivo, config in self.batch_files.items():
        sheets = config["sheets"]
        vars = config["vars"]
        
        # Seleccionar hojas activadas
        selected_sheets = [
            sheets[name] 
            for name, var in vars.items() 
            if var.get()
        ]
        
        # Concatenar hojas de este archivo
        if selected_sheets:
            archivo_df = pd.concat(selected_sheets, ignore_index=True)
            all_dfs.append(archivo_df)
    
    # Consolidar todo
    final = pd.concat(all_dfs, ignore_index=True)
    
    # Guardar
    path = filedialog.asksaveasfilename(defaultextension=".xlsx")
    final.to_excel(path, index=False)
    
    messagebox.showinfo("Éxito", f"Guardado: {len(final)} filas")
```

### Consideraciones

| Aspecto | Detalle |
|--------|---------|
| **Memoria** | Carga TODOS los DataFrames en memoria |
| **Validación** | No valida duplicados de ID |
| **Orden** | Mantiene orden de hojas cargadas |
| **Índices** | `ignore_index=True` renumera filas |
| **Errores** | Si hay error, mensajebox y retorna |

---

## Módulo: Merge Files

### Propósito
Consolidar múltiples archivos Excel/CSV en uno solo, concatenando TODAS las filas.

### Diferencia con Union Sheets
```
Union Sheets:    Múltiples archivos → Múltiples hojas/archivo → Combina selección
Merge Files:     Múltiples archivos → Cada uno completo → Un solo archivo
```

### Caso de uso
```
Tengo 50 archivos CSV de ventas diarias.
Quiero combinarlos en un único Excel para análisis global.

Solución:
  1. Seleccionar los 50 archivos
  2. Leer cada uno como DataFrame
  3. Concatenar todos
  4. Guardar resultado
```

### Código clave

```python
def _run(self):
    if not self._files:
        return
    
    all_dfs = []
    
    for file_path in self._files:
        try:
            if file_path.endswith(".csv"):
                # Leer CSV
                df = pd.read_csv(file_path)
            else:
                # Leer Excel (TODAS las hojas de este archivo)
                sheets_dict = pd.read_excel(file_path, sheet_name=None)
                # Concatenar hojas del mismo archivo
                df = pd.concat(sheets_dict.values(), ignore_index=True)
            
            all_dfs.append(df)
        
        except Exception as e:
            messagebox.showerror("Error", f"{os.path.basename(file_path)}: {e}")
            return
    
    # Consolidación final
    final = pd.concat(all_dfs, ignore_index=True)
    
    # Diálogo guardar
    path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel", "*.xlsx")]
    )
    
    if path:
        final.to_excel(path, index=False)
        messagebox.showinfo("Éxito", f"Guardado: {len(final)} filas totales.")
        self.status.set(f"Consolidado: {len(final)} filas.")
```

### Flujo visual

```
archivo1.csv    archivo2.xlsx   archivo3.csv
    ↓               ↓                ↓
 DataFrame        [Hoja1]          DataFrame
    +             [Hoja2]      +
    |             [Hoja3]      |
    |                ↓         |
    |            concat       |
    |                ↓         |
    └─────→ concatenados ←────┘
                  ↓
            final DataFrame
                  ↓
            Excel único
```

---

## Módulo: Split Sheets

### Propósito
Dividir un archivo Excel (con múltiples hojas) en múltiples archivos (uno por hoja).

### Opuesto de Union Sheets
```
Union:    múltiples archivos → 1 archivo consolidado
Split:    1 archivo → múltiples archivos
```

### Caso de uso
```
Tengo un Excel "datos.xlsx" con 10 hojas (una por región).
Quiero separarlas: región1.xlsx, región2.xlsx, ... región10.xlsx

Solución:
  1. Abrir datos.xlsx
  2. Para cada hoja:
     - Crear archivo separado
     - Guardar solo esa hoja
```

### Código clave

```python
def _load(self):
    # Cargar archivo
    path = filedialog.askopenfilename(
        filetypes=[("Excel", "*.xlsx *.xlsm")]
    )
    
    # Leer TODAS las hojas
    self._df_dict = pd.read_excel(path, sheet_name=None)
    # Resultado: {"Hoja1": df, "Hoja2": df, ...}
    
    # Dibujar checkboxes para seleccionar hojas
    for name in self._df_dict:
        var = tk.BooleanVar(value=True)
        self._sheet_vars[name] = var
        # dibujar checkbox...

def _run(self):
    # Obtener hojas seleccionadas
    selected = [n for n, v in self._sheet_vars.items() if v.get()]
    
    # Elegir carpeta destino
    folder = filedialog.askdirectory()
    
    # Guardar cada hoja como archivo separado
    for sheet_name in selected:
        # Limpiar nombre (eliminar caracteres especiales)
        clean_name = "".join(
            c for c in sheet_name 
            if c.isalnum() or c in " _"
        ).strip()
        
        # Guardar
        output_path = os.path.join(folder, f"{clean_name}.xlsx")
        self._df_dict[sheet_name].to_excel(output_path, index=False)
```

### Flujo

```
Excel entrada con N hojas
    ├─ Hoja1 → hoja1.xlsx (N filas)
    ├─ Hoja2 → hoja2.xlsx (M filas)
    ├─ Hoja3 → hoja3.xlsx (K filas)
    └─ HojaX → hojaX.xlsx (J filas)
```

### Validaciones

```python
if not selected:
    messagebox.showwarning("Atención", 
                          "Selecciona al menos una hoja.")
    return

if not folder:
    # Usuario canceló diálogo
    return
```

---

## Módulo: Filter Module

### Propósito
Aplicar filtros inteligentes, ordenamientos y seleccionar columnas de un DataFrame.

### Características principales

1. **Detección de tipo de dato**
   ```python
   def _col_kind(series: pd.Series) -> str:
       if pd.api.types.is_numeric_dtype(series):
           return "numeric"
       try:
           converted = pd.to_datetime(series, errors="coerce")
           if converted.notna().mean() > 0.7:
               return "datetime"
       except:
           pass
       return "text"
   ```
   
2. **Panel de filtro por columna** (`ColumnFilterPanel`)
   - Colapsable (click en header abre/cierra)
   - Interfaz diferente según tipo:
     - **Text**: Checkboxes + búsqueda
     - **Numeric**: Min/Max fields
     - **Datetime**: Date range picker

3. **Validación en tiempo real**
   - Preview vivo mientras configuras

### Arquitectura de ColumnFilterPanel

```python
class ColumnFilterPanel(tk.Frame):
    def __init__(self, parent, col, series, on_change):
        self.col = col
        self.series = series
        self.kind = _col_kind(series)  # ← Detecta tipo
        
        self._check_vars = {}  # Para text filters
        self._num_min = tk.StringVar()  # Para numeric
        self._num_max = tk.StringVar()
        self._date_from = tk.StringVar()  # Para datetime
        self._date_to = tk.StringVar()
        self._search_var = tk.StringVar()
        
        self._build()
    
    def _build(self):
        # Header colapsable
        hdr = tk.Frame(...)
        self._arrow = tk.Label(hdr, text="▶")  # ← Click para expandir
        
        # Body (colapsable)
        self._body = tk.Frame(...)
        
        if self.kind == "text":
            self._build_text_filter()
        elif self.kind == "numeric":
            self._build_numeric_filter()
        elif self.kind == "datetime":
            self._build_date_filter()
    
    def _toggle(self, event):
        if self._expanded:
            self._body.pack_forget()
            self._arrow.config(text="▶")
        else:
            self._body.pack()
            self._arrow.config(text="▼")
        self._expanded = not self._expanded
```

### Ejemplo: Text Filter

```python
def _build_text_filter(self):
    # Búsqueda
    search_e = tk.Entry(self._body, textvariable=self._search_var)
    search_e.pack(fill="x")
    
    # Botones seleccionar/deseleccionar
    GhostBtn(self._body, "✓ Todo", command=self._select_all).pack()
    GhostBtn(self._body, "✗ Nada", command=self._deselect_all).pack()
    
    # Checkboxes dinámicos
    self._cb_scroll = ScrollableFrame(self._body)
    self._cb_scroll.pack(fill="x")
    self._refresh_checkboxes()

def _refresh_checkboxes(self):
    """Dibuja checkboxes basado en búsqueda"""
    # Limpiar
    for w in self._cb_scroll.inner.winfo_children():
        w.destroy()
    
    # Valores únicos de la columna
    search_term = self._search_var.get().lower()
    unique_values = self.series.dropna().unique()
    
    # Dibujar checkboxes que coincidan con búsqueda
    for value in unique_values:
        if search_term not in str(value).lower():
            continue
        
        if value not in self._check_vars:
            self._check_vars[value] = tk.BooleanVar(value=True)
        
        cb = tk.Checkbutton(
            self._cb_scroll.inner,
            text=str(value),
            variable=self._check_vars[value],
            command=self.on_change
        )
        cb.pack(anchor="w")
```

### Flujo de aplicación de filtros

```python
def _apply_filters(self):
    df = self._original_df.copy()
    
    for col_name, panel in self._filter_panels.items():
        if panel.kind == "text":
            # Obtener valores seleccionados
            selected = [v for v, var in panel._check_vars.items() 
                       if var.get()]
            df = df[df[col_name].isin(selected)]
        
        elif panel.kind == "numeric":
            min_val = panel._num_min.get()
            max_val = panel._num_max.get()
            
            if min_val:
                df = df[df[col_name] >= float(min_val)]
            if max_val:
                df = df[df[col_name] <= float(max_val)]
        
        elif panel.kind == "datetime":
            # Similar a numeric pero con fechas
            pass
    
    # Aplicar ordenamiento
    sort_cols = [o["col"] for o in self._sort_order]
    if sort_cols:
        df = df.sort_values(by=sort_cols)
    
    # Seleccionar columnas
    selected_cols = [c for c, var in self._col_vars.items() 
                    if var.get()]
    df = df[selected_cols]
    
    return df
```

### Performance considerations
```
⚠️ Con 100k filas y 50 columnas, los filtros son LENTOS
   → Considera caché: solo recalcular si cambió algo
   → Preview solo primeras 1000 filas
   → Usar "Apply" button en lugar de tiempo real
```

---

## Sistema de Estilos

### Jerarquía de importación

```python
# En cualquier módulo:
from app.ui import styles as s

# Luego uses:
s.C_RED          # Color
s.F_H1           # Fuente
s.PAD_LG         # Dimensión
```

### Mapeo de colores para estados

```python
# Botones
PrimaryBtn   → bg=C_RED, hover=C_RED_DK
SecondaryBtn → bg=C_BG_CARD (blanco)
GhostBtn     → bg=C_BG (gris muy claro)

# Fondos
Headers      → C_DARK (gris oscuro)
Content      → C_BG (gris muy claro)
Cards        → C_BG_CARD (blanco)

# Estados
Success      → C_SUCCESS (verde)
Warning      → C_WARN (naranja)
Info         → C_INFO (azul)
Active       → C_RED (rojo)
```

### Extensión de estilos

Si necesitas agregar un nuevo color:

```python
# app/ui/styles.py
C_MY_COLOR = "#XXXXXX"

# En componentes
class MyComponent(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=s.C_MY_COLOR)
```

---

## Gestión de Estado

### Patrones de estado

#### 1. Estado Simple (variables tk)
```python
class MiScreen(BaseScreen):
    def build_body(self, parent):
        self._value = tk.StringVar()
        entry = tk.Entry(parent, textvariable=self._value)
        entry.pack()
    
    def _get_value(self):
        return self._value.get()
```

#### 2. Estado Complejo (diccionario)
```python
class UnionSheetsScreen(BaseScreen):
    def __init__(self, container, router):
        super().__init__(container, router)
        self.batch_files = {}  # ← Estado centralizado
    
    def _load_files(self):
        # Modificar estado
        self.batch_files[path] = {
            "sheets": data,
            "vars": vars_dict
        }
```

#### 3. Sincronización Listener
```python
class FilterScreen(BaseScreen):
    def build_body(self, parent):
        self._value = tk.StringVar()
        
        # Reaccionar a cambios
        self._value.trace_add("write", self._on_change)
    
    def _on_change(self, *args):
        # Se llama cada vez que _value cambia
        self.status.set(f"Valor: {self._value.get()}")
```

### Anti-patterns

❌ No hagas esto:
```python
# Modificar label directamente
label.config(text="nuevo")

# Mejor: usar variable y label con textvariable
var = tk.StringVar(value="nuevo")
label = tk.Label(parent, textvariable=var)
var.set("otro valor")  # Actualiza label automáticamente
```

❌ No guardes DataFrames grandes en estado
```python
# Malo
self._all_data = pd.read_excel("1GB_file.xlsx")

# Mejor: Procesarlos on-demand
def _process(self):
    df = pd.read_excel("1GB_file.xlsx")
    # Procesar inmediatamente
    result = df.groupby(...)
```

---

## Flujo Completo: Usuario hace clic en "Unir Sheets"

```
1. MenuScreen._on_card_click()
   └─ self._navigate("union_sheets")

2. MenuScreen._navigate()
   ├─ from .union_sheets import UnionSheetsScreen
   ├─ MAP["union_sheets"] = UnionSheetsScreen
   └─ self.router.navigate(UnionSheetsScreen)

3. Router.navigate(UnionSheetsScreen)
   ├─ self._clear()  # Destruye MenuScreen widgets
   ├─ self._current = UnionSheetsScreen(self.container, self)
   └─ self._current.render()

4. UnionSheetsScreen.render()
   ├─ self._build_shell()  # BaseScreen
   │  ├─ top_bar ← [BackBtn] [Título] [toolbar]
   │  ├─ divider
   │  ├─ body ← empty frame
   │  └─ status ← StatusBar
   │
   └─ self.build_body(self.body)  # override
      ├─ action_bar ← [Cargar archivos] [Consolidar]
      ├─ divider
      ├─ pane
      │  ├─ left ← listbox de archivos
      │  └─ right ← config: nombre salida + checkboxes hojas
      └─ widgets listos para interacción

5. Usuario clickea [Cargar archivos]
   └─ _load_files()
      ├─ filedialog.askopenfilenames()
      ├─ para cada ruta:
      │  ├─ df_dict = pd.read_excel(ruta, sheet_name=None)
      │  └─ batch_files[ruta] = {sheets, vars, out_name}
      ├─ actualizar listbox
      └─ status.set("3 archivo(s) cargado(s)")

6. Usuario selecciona archivo en listbox
   └─ _on_select()
      ├─ obtener ruta seleccionada
      ├─ limpiar _sheets_scroll
      └─ dibujar checkboxes de hojas
           [✓] Hoja1 (100 filas)
           [✓] Hoja2 (200 filas)

7. Usuario cambia nombre salida
   └─ _update_out_name() [KeyRelease listener]
      ├─ batch_files[sel_path]["out_name"] = nuevo_nombre
      └─ _btn_process.config(state="normal")

8. Usuario clickea [Consolidar y guardar]
   └─ _process()
      ├─ para cada archivo en batch_files:
      │  ├─ selected_sheets = [df para hojas con checkmark]
      │  └─ archivo_result = pd.concat(selected_sheets)
      ├─ final = pd.concat([archivo_result, ...])
      ├─ filedialog.asksaveasfilename()
      ├─ final.to_excel(path)
      ├─ messagebox.showinfo("Éxito", "...")
      └─ status.set("Consolidado: XXX filas")

9. Usuario clickea [← VOLVER]
   └─ BackBtn command:
      └─ self.router.navigate(MenuScreen)
          ├─ _clear()  # Destruye UnionSheetsScreen
          └─ MenuScreen renderizado de nuevo
```

---

**Última actualización:** 21 abril 2026  
**Nivel técnico:** Avanzado
