# 📊 DIAGRAMAS VISUALES — FastEditable v2.0

## Diagrama 1: Flujo General de la Aplicación

```mermaid
graph TD
    A[main.py<br/>Punto de entrada] -->|instancia| B[FastEditableApp]
    B -->|crea| C[Tkinter Root]
    B -->|crea| D[Router]
    D -->|navega a| E[MenuScreen]
    
    E -->|clic opción 1| F[UnionSheetsScreen]
    E -->|clic opción 2| G[MergeFilesScreen]
    E -->|clic opción 3| H[SplitSheetsScreen]
    E -->|clic opción 4| I[FilterScreen]
    
    F -->|volver| E
    G -->|volver| E
    H -->|volver| E
    I -->|volver| E
    
    style A fill:#E31937,stroke:#B5122B,color:#fff
    style E fill:#FFC0C0,stroke:#E31937
    style F fill:#E8F5E9,stroke:#1A7F4B
    style G fill:#E8F5E9,stroke:#1A7F4B
    style H fill:#E8F5E9,stroke:#1A7F4B
    style I fill:#E8F5E9,stroke:#1A7F4B
```

## Diagrama 2: Arquitectura de Capas

```mermaid
graph TB
    subgraph "Presentación (UI)"
        A["🎨 Styles<br/>(Colores, fuentes)"]
        B["🔘 Components<br/>(Botones, Cards, etc)"]
        C["📐 Layouts<br/>(BaseScreen)"]
    end
    
    subgraph "Lógica (Módulos)"
        D["MenuScreen<br/>(Menú principal)"]
        E["UnionSheetsScreen<br/>(Unir hojas)"]
        F["MergeFilesScreen<br/>(Unir archivos)"]
        G["SplitSheetsScreen<br/>(Separar hojas)"]
        H["FilterScreen<br/>(Filtrar datos)"]
    end
    
    subgraph "Núcleo (Core)"
        I["⚙️ Router<br/>(Navegación)"]
        J["🔧 Config<br/>(Constantes)"]
    end
    
    subgraph "Librerías Externas"
        K["📊 Pandas"]
        L["🗂️ File Dialog"]
        M["⚠️ MessageBox"]
    end
    
    D --> C
    E --> C
    F --> C
    G --> C
    H --> C
    
    C --> B
    B --> A
    A --> J
    B --> J
    
    D --> I
    E --> I
    F --> I
    G --> I
    H --> I
    I --> J
    
    E --> K
    F --> K
    G --> K
    H --> K
    
    E --> L
    F --> L
    G --> L
    H --> L
    
    E --> M
    F --> M
    G --> M
    H --> M
    
    style A fill:#F2F3F5,stroke:#53565A
    style B fill:#F2F3F5,stroke:#53565A
    style C fill:#F2F3F5,stroke:#53565A
    style D fill:#E8F5E9,stroke:#1A7F4B
    style E fill:#E8F5E9,stroke:#1A7F4B
    style F fill:#E8F5E9,stroke:#1A7F4B
    style G fill:#E8F5E9,stroke:#1A7F4B
    style H fill:#E8F5E9,stroke:#1A7F4B
    style I fill:#FFF3CD,stroke:#D97706
    style J fill:#FFF3CD,stroke:#D97706
    style K fill:#E3F2FD,stroke:#1D6FBF
    style L fill:#E3F2FD,stroke:#1D6FBF
    style M fill:#E3F2FD,stroke:#1D6FBF
```

## Diagrama 3: Herencia de Pantallas

```mermaid
graph TD
    A["BaseScreen<br/>(Plantilla abstracta)<br/>- top_bar<br/>- body<br/>- status_bar"]
    
    B["MenuScreen<br/>(Diseño propio)"]
    C["UnionSheetsScreen"]
    D["MergeFilesScreen"]
    E["SplitSheetsScreen"]
    F["FilterScreen"]
    
    A -->|heredado| C
    A -->|heredado| D
    A -->|heredado| E
    A -->|heredado| F
    
    style A fill:#FFF3CD,stroke:#D97706,color:#000
    style B fill:#FFE8E8,stroke:#E31937
    style C fill:#E8F5E9,stroke:#1A7F4B
    style D fill:#E8F5E9,stroke:#1A7F4B
    style E fill:#E8F5E9,stroke:#1A7F4B
    style F fill:#E8F5E9,stroke:#1A7F4B
```

## Diagrama 4: Flujo de UnionSheets (Detallado)

```mermaid
graph LR
    A["📂 Cargar<br/>múltiples<br/>archivos"] -->|xlsx/csv| B["📊 Detectar<br/>hojas"]
    
    B -->|por archivo| C["☑️ Seleccionar<br/>hojas"]
    
    C -->|configurar| D["💾 Especificar<br/>nombre<br/>salida"]
    
    D -->|procesar| E["🔗 Concatenar<br/>DataFrames"]
    
    E -->|guardar| F["✅ Archivo<br/>consolidado"]
    
    style A fill:#E3F2FD,stroke:#1D6FBF
    style B fill:#E3F2FD,stroke:#1D6FBF
    style C fill:#E3F2FD,stroke:#1D6FBF
    style D fill:#E3F2FD,stroke:#1D6FBF
    style E fill:#E3F2FD,stroke:#1D6FBF
    style F fill:#C8E6C9,stroke:#1A7F4B
```

## Diagrama 5: Flujo de FilterModule (Avanzado)

```mermaid
graph LR
    A["📂 Cargar<br/>archivo"] -->|analizar| B["🔍 Detectar<br/>tipo datos"]
    
    B -->|clasificar| C["📝 Crear<br/>paneles<br/>filtro"]
    
    C -->|por tipo| D["Texto<br/>Checkboxes"]
    C -->|por tipo| E["Número<br/>Min/Max"]
    C -->|por tipo| F["📅 Fecha<br/>Rango"]
    
    D --> G["⚙️ Aplicar<br/>filtros"]
    E --> G
    F --> G
    
    G -->|ordenar| H["📊 Reordenar<br/>datos"]
    
    H -->|seleccionar| I["📋 Elegir<br/>columnas"]
    
    I -->|vista previa| J["👁️ Preview<br/>en vivo"]
    
    J -->|guardar| K["✅ Resultado<br/>filtrado"]
    
    style A fill:#E3F2FD,stroke:#1D6FBF
    style B fill:#E3F2FD,stroke:#1D6FBF
    style C fill:#E3F2FD,stroke:#1D6FBF
    style D fill:#FFF3CD,stroke:#D97706
    style E fill:#FFF3CD,stroke:#D97706
    style F fill:#FFF3CD,stroke:#D97706
    style G fill:#FFF3CD,stroke:#D97706
    style H fill:#FFF3CD,stroke:#D97706
    style I fill:#FFF3CD,stroke:#D97706
    style J fill:#FFF3CD,stroke:#D97706
    style K fill:#C8E6C9,stroke:#1A7F4B
```

## Diagrama 6: Estructura de Archivos

```mermaid
graph TD
    A["📦 FastEditable_v2/"]
    
    A -->|config| B["main.py"]
    A -->|docs| C["README.md"]
    A -->|docs| D["MAPEO_PROGRAMA.md"]
    
    A -->|código| E["🗂️ app/"]
    
    E -->|núcleo| F["🗂️ core/"]
    F -->|config global| G["config.py"]
    F -->|navegación| H["router.py"]
    
    E -->|interfaz| I["🗂️ ui/"]
    I -->|estilos| J["styles.py"]
    I -->|componentes| K["components.py"]
    I -->|plantillas| L["layouts.py"]
    
    E -->|funcionalidad| M["🗂️ modules/"]
    M -->|menú| N["menu.py"]
    M -->|módulo 1| O["union_sheets.py"]
    M -->|módulo 2| P["merge_files.py"]
    M -->|módulo 3| Q["split_sheets.py"]
    M -->|módulo 4| R["filter_module.py"]
    
    style A fill:#E31937,stroke:#B5122B,color:#fff
    style B fill:#FFF3CD,stroke:#D97706
    style C fill:#FFF3CD,stroke:#D97706
    style D fill:#FFF3CD,stroke:#D97706
    style E fill:#E8F5E9,stroke:#1A7F4B
    style F fill:#E3F2FD,stroke:#1D6FBF
    style G fill:#E3F2FD,stroke:#1D6FBF
    style H fill:#E3F2FD,stroke:#1D6FBF
    style I fill:#E3F2FD,stroke:#1D6FBF
    style J fill:#E3F2FD,stroke:#1D6FBF
    style K fill:#E3F2FD,stroke:#1D6FBF
    style L fill:#E3F2FD,stroke:#1D6FBF
    style M fill:#F8BBD0,stroke:#E31937
    style N fill:#F8BBD0,stroke:#E31937
    style O fill:#F8BBD0,stroke:#E31937
    style P fill:#F8BBD0,stroke:#E31937
    style Q fill:#F8BBD0,stroke:#E31937
    style R fill:#F8BBD0,stroke:#E31937
```

## Diagrama 7: Ciclo de Render

```mermaid
graph TD
    A["Router.navigate<br/>(ScreenClass)"] -->|instancia| B["ScreenClass<br/>.__init__()"]
    
    B -->|llamada| C["screen.render()"]
    
    C -->|heredado| D["_build_shell<br/>(BaseScreen)"]
    
    D -->|construye| E["top_bar<br/>← VOLVER + Título"]
    D -->|construye| F["divider"]
    D -->|construye| G["body frame<br/>vacío"]
    D -->|construye| H["status_bar"]
    
    C -->|llamada| I["build_body<br/>(override)"]
    
    I -->|rellena| G
    
    J["Resultado final<br/>en pantalla"] ← E
    J ← F
    J ← G
    J ← H
    
    style A fill:#FFC0C0,stroke:#E31937
    style B fill:#FFC0C0,stroke:#E31937
    style C fill:#E3F2FD,stroke:#1D6FBF
    style D fill:#E3F2FD,stroke:#1D6FBF
    style E fill:#FFF3CD,stroke:#D97706
    style F fill:#FFF3CD,stroke:#D97706
    style G fill:#C8E6C9,stroke:#1A7F4B
    style H fill:#FFF3CD,stroke:#D97706
    style I fill:#F8BBD0,stroke:#E31937
    style J fill:#C8E6C9,stroke:#1A7F4B
```

## Diagrama 8: Flujo de Datos (Pandas)

```mermaid
graph LR
    A["Archivo(s)"] -->|pd.read_excel<br/>pd.read_csv| B["DataFrame(s)"]
    
    B -->|seleccionar| C["Filtrar columnas"]
    C -->|aplicar| D["Aplicar filtros"]
    D -->|ordenar| E["Ordenar filas"]
    E -->|combinar| F["Concatenar datos"]
    F -->|guardar| G["df.to_excel<br/>df.to_csv"]
    
    G -->|resultado| H["Archivo salida"]
    
    style A fill:#E3F2FD,stroke:#1D6FBF
    style B fill:#DBEAFE,stroke:#1D6FBF
    style C fill:#DBEAFE,stroke:#1D6FBF
    style D fill:#DBEAFE,stroke:#1D6FBF
    style E fill:#DBEAFE,stroke:#1D6FBF
    style F fill:#DBEAFE,stroke:#1D6FBF
    style G fill:#DBEAFE,stroke:#1D6FBF
    style H fill:#C8E6C9,stroke:#1A7F4B
```

## Diagrama 9: Componentes UI Reutilizables

```mermaid
graph TD
    A["🎨 UI Components"]
    
    A -->|Botones| B["PrimaryBtn<br/>(rojo fondo)"]
    A -->|Botones| C["SecondaryBtn<br/>(borde)"]
    A -->|Botones| D["GhostBtn<br/>(transparente)"]
    A -->|Botones| E["BackBtn<br/>(← VOLVER)"]
    
    A -->|Etiquetas| F["H1, H2<br/>(Títulos)"]
    A -->|Etiquetas| G["BodyLabel<br/>(Texto)"]
    A -->|Etiquetas| H["Badge<br/>(Chips color)"]
    
    A -->|Contenedores| I["Card<br/>(Frame blanco)"]
    A -->|Contenedores| J["ScrollableFrame<br/>(Scrollbar)"]
    A -->|Contenedores| K["Divider<br/>(Línea)"]
    
    A -->|Estado| L["StatusBar<br/>(Pie)"]
    
    style A fill:#E31937,stroke:#B5122B,color:#fff
    style B fill:#FFC0C0,stroke:#E31937
    style C fill:#FFC0C0,stroke:#E31937
    style D fill:#FFC0C0,stroke:#E31937
    style E fill:#FFC0C0,stroke:#E31937
    style F fill:#FFF3CD,stroke:#D97706
    style G fill:#FFF3CD,stroke:#D97706
    style H fill:#FFF3CD,stroke:#D97706
    style I fill:#F8BBD0,stroke:#E31937
    style J fill:#F8BBD0,stroke:#E31937
    style K fill:#F8BBD0,stroke:#E31937
    style L fill:#C8E6C9,stroke:#1A7F4B
```

---

**Notas:**
- 🔴 Rojo (#E31937): Elementos principales
- 🟠 Naranja (#D97706): Configuración/núcleo
- 🟢 Verde (#1A7F4B): Éxito/resultado
- 🔵 Azul (#1D6FBF): Entrada/procesamiento
- 🟡 Amarillo (#D97706): Estado/transición
