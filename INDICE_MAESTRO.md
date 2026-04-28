# 📚 ÍNDICE MAESTRO — FILTER v2.0

**Documentación completa del programa**

---

## 📌 Documentos Disponibles

### 1️⃣ [MAPEO_PROGRAMA.md](MAPEO_PROGRAMA.md) — Mapeo General
**Para:** Entender la estructura general del programa  
**Contiene:**
- ✅ Visión general del proyecto
- ✅ Arquitectura del sistema
- ✅ Estructura de carpetas
- ✅ Flujo de navegación
- ✅ Descripción de cada módulo
- ✅ Sistema de UI (estilos, componentes, layouts)
- ✅ Flujo de datos
- ✅ Stack tecnológico
- ✅ Convenciones de código

**Lectura recomendada:** 15-20 minutos  
**Público:** Todos (principiantes a avanzados)

---

### 2️⃣ [DIAGRAMAS_VISUALES.md](DIAGRAMAS_VISUALES.md) — Visualización
**Para:** Ver representaciones gráficas del programa  
**Contiene:**
- ✅ Flujo general de la aplicación
- ✅ Arquitectura de capas
- ✅ Herencia de pantallas
- ✅ Flujos detallados por módulo
- ✅ Estructura de archivos
- ✅ Ciclo de render
- ✅ Flujo de datos con Pandas
- ✅ Componentes UI

**Lectura recomendada:** 10 minutos (visual)  
**Público:** Principiantes, visual learners

---

### 3️⃣ [REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md) — Cheat Sheet
**Para:** Consulta rápida mientras codificas  
**Contiene:**
- ✅ Tabla de archivos principales
- ✅ Cómo ejecutar
- ✅ Paleta de colores completa
- ✅ Tipografía
- ✅ Componentes disponibles (botones, etiquetas, contenedores)
- ✅ Estructura de pantalla base
- ✅ Navegación
- ✅ Operaciones Pandas comunes
- ✅ Patrones comunes
- ✅ Debug
- ✅ Variables comunes
- ✅ Dimensiones estándar
- ✅ Errores comunes
- ✅ Tips de rendimiento

**Lectura recomendada:** Bajo demanda  
**Público:** Desarrolladores

---

### 4️⃣ [ANALISIS_TECNICO.md](ANALISIS_TECNICO.md) — Análisis Profundo
**Para:** Entender en detalle cómo funciona cada componente  
**Contiene:**
- ✅ Sistema de Router (cómo navega)
- ✅ BaseScreen - Arquitectura (plantilla de pantallas)
- ✅ Módulo Union Sheets (análisis código)
- ✅ Módulo Merge Files
- ✅ Módulo Split Sheets
- ✅ Módulo Filter Module (componentes avanzados)
- ✅ Sistema de Estilos (jerarquía)
- ✅ Gestión de Estado
- ✅ Flujo completo: usuario hace clic

**Lectura recomendada:** 25-30 minutos  
**Público:** Desarrolladores avanzados

---

## 🎯 Guía de Lectura Recomendada

### Para Principiantes
1. **Inicio:** [MAPEO_PROGRAMA.md](MAPEO_PROGRAMA.md) - Secciones:
   - Visión General
   - Arquitectura del Sistema
   - Estructura de Carpetas
   - Módulos Principales (solo lectura, sin código)

2. **Visualización:** [DIAGRAMAS_VISUALES.md](DIAGRAMAS_VISUALES.md)
   - Mirar todos los diagramas

3. **Referencia:** [REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md)
   - Guardar en favoritos

**Tiempo total:** ~45 minutos

---

### Para Desarrolladores Intermedios
1. **Mapeo completo:** [MAPEO_PROGRAMA.md](MAPEO_PROGRAMA.md) - Secciones:
   - Todo (incluida la jerarquía)

2. **Análisis técnico:** [ANALISIS_TECNICO.md](ANALISIS_TECNICO.md) - Secciones:
   - Sistema de Router
   - BaseScreen

3. **Referencia rápida:** [REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md)
   - Enfoque en "Patrones comunes"

**Tiempo total:** ~1-2 horas

---

### Para Desarrolladores Avanzados
1. Leer todo en profundidad:
   - [MAPEO_PROGRAMA.md](MAPEO_PROGRAMA.md) (código esencial)
   - [ANALISIS_TECNICO.md](ANALISIS_TECNICO.md) (pseudocódigo)
   - [REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md) (APIs)

2. Leer código fuente directamente en los archivos `.py`

**Tiempo total:** ~2-3 horas + exploración código

---

## 📂 Estructura Rápida

```
FastEditable_v2/
│
├── 📖 DOCUMENTACIÓN
│   ├── MAPEO_PROGRAMA.md ............... Mapeo general completo
│   ├── DIAGRAMAS_VISUALES.md ........... 9 diagramas Mermaid
│   ├── REFERENCIA_RAPIDA.md ........... Cheat sheet
│   ├── ANALISIS_TECNICO.md ............ Análisis profundo
│   └── INDICE_MAESTRO.md .............. Este archivo
│
├── 📄 CÓDIGO
│   ├── main.py ........................ Punto de entrada
│   └── app/
│       ├── core/
│       │   ├── config.py .............. Constantes
│       │   └── router.py .............. Navegación
│       ├── ui/
│       │   ├── styles.py .............. Estilos
│       │   ├── components.py .......... Widgets
│       │   └── layouts.py ............. Plantilla
│       └── modules/
│           ├── menu.py ................ Menú principal
│           ├── union_sheets.py ........ Módulo 1
│           ├── merge_files.py ......... Módulo 2
│           ├── split_sheets.py ........ Módulo 3
│           └── filter_module.py ....... Módulo 4
│
└── 📋 README.md ....................... Documentación básica
```

---

## 🔍 Búsqueda Rápida por Tema

### Quiero entender...

| Tema | Documento | Sección |
|------|-----------|---------|
| **Estructura general** | MAPEO_PROGRAMA | Visión General / Arquitectura |
| **Cómo navega entre pantallas** | MAPEO_PROGRAMA | Flujo de Navegación |
| **Qué archivos hay** | MAPEO_PROGRAMA | Estructura de Carpetas |
| **Qué es cada módulo** | MAPEO_PROGRAMA | Módulos Principales |
| **Sistema de estilos** | MAPEO_PROGRAMA | Sistema de UI |
| **Cómo se heredan pantallas** | ANALISIS_TECNICO | BaseScreen |
| **Cómo funciona Union Sheets** | ANALISIS_TECNICO | Módulo Union Sheets |
| **Cómo funciona Filter** | ANALISIS_TECNICO | Módulo Filter Module |
| **Colores disponibles** | REFERENCIA_RAPIDA | Paleta de Colores |
| **Componentes UI** | REFERENCIA_RAPIDA | Componentes Disponibles |
| **Cómo hacer un nuevo módulo** | REFERENCIA_RAPIDA | Checklist: Crear Nuevo Módulo |
| **Operaciones Pandas** | REFERENCIA_RAPIDA | Operaciones Pandas Comunes |
| **Errores comunes** | REFERENCIA_RAPIDA | Errores Comunes |
| **Flujo completo de un clic** | ANALISIS_TECNICO | Flujo Completo: Usuario hace clic |
| **Diagramas visuales** | DIAGRAMAS_VISUALES | Cualquier sección |

---

## 🚀 Casos de Uso

### "Necesito modificar un módulo existente"
1. Lee la sección del módulo en [ANALISIS_TECNICO.md](ANALISIS_TECNICO.md)
2. Abre el código fuente en el editor
3. Usa [REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md) para APIs
4. Ejecuta y prueba: `python main.py`

### "Necesito crear un módulo nuevo"
1. Lee [REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md) → "Checklist: Crear Nuevo Módulo"
2. Copia estructura de un módulo existente
3. Personaliza `build_body()`
4. Registra en MenuScreen

### "Necesito cambiar estilos/colores"
1. Abre [REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md) → "Paleta de Colores"
2. Edita `app/ui/styles.py`
3. Importa cambios: `from app.ui import styles as s`

### "Necesito entender un flujo específico"
1. Ve a [DIAGRAMAS_VISUALES.md](DIAGRAMAS_VISUALES.md)
2. Busca el diagrama relevante
3. Lee la sección correspondiente en [ANALISIS_TECNICO.md](ANALISIS_TECNICO.md)

### "Necesito debugear un error"
1. Consulta [REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md) → "Errores Comunes"
2. Lee la sección Debug
3. Agrega `print()` o usa `self.status.set()` para feedback

---

## 📊 Estadísticas de Documentación

| Documento | Párrafos | Secciones | Código | Diagramas |
|-----------|----------|-----------|--------|-----------|
| MAPEO_PROGRAMA.md | ~150 | 11 | Sí | 2 |
| DIAGRAMAS_VISUALES.md | ~30 | 9 | No | 9 |
| REFERENCIA_RAPIDA.md | ~200 | 15 | Sí | 0 |
| ANALISIS_TECNICO.md | ~250 | 8 | Sí | 0 |
| **TOTAL** | **~630** | **~43** | **Sí** | **11** |

---

## 🎓 Conceptos Clave

### 1. Router Pattern
Sistema de navegación que gestiona qué pantalla se muestra. Es el "controlador" central.

**Documentos:** [MAPEO_PROGRAMA](MAPEO_PROGRAMA.md#-flujo-de-navegación) → [ANALISIS_TECNICO](ANALISIS_TECNICO.md#sistema-de-router)

### 2. Herencia BaseScreen
Todas las pantallas heredan de una clase base que define la estructura fija.

**Documentos:** [MAPEO_PROGRAMA](MAPEO_PROGRAMA.md#-sistema-de-ui) → [ANALISIS_TECNICO](ANALISIS_TECNICO.md#basescreen---arquitectura)

### 3. Gestión de Estado
Usar variables Tkinter y diccionarios para manejar datos de la pantalla.

**Documentos:** [ANALISIS_TECNICO](ANALISIS_TECNICO.md#gestión-de-estado)

### 4. Pandas para Datos
Biblioteca para leer, transformar y guardar DataFrames.

**Documentos:** [REFERENCIA_RAPIDA](REFERENCIA_RAPIDA.md#-operaciones-pandas-comunes)

### 5. Sistema de Estilos
Centralizar colores, fuentes y dimensiones en un archivo único.

**Documentos:** [ANALISIS_TECNICO](ANALISIS_TECNICO.md#sistema-de-estilos)

---

## ✅ Checklist de Comprensión

Después de leer esta documentación, deberías poder:

- [ ] Explicar qué hace cada módulo
- [ ] Navegar el código fuente sin perderte
- [ ] Crear una nueva pantalla desde cero
- [ ] Modificar estilos y colores
- [ ] Entender cómo fluyen los datos
- [ ] Debugear problemas comunes
- [ ] Usar componentes UI existentes
- [ ] Escribir código siguiendo convenciones
- [ ] Agregar nuevas funcionalidades
- [ ] Documentar cambios

---

## 🔗 Links Útiles

### Dentro del Proyecto
- [README.md](README.md) — Información básica
- [MAPEO_PROGRAMA.md](MAPEO_PROGRAMA.md) — Mapeo general
- [DIAGRAMAS_VISUALES.md](DIAGRAMAS_VISUALES.md) — Visualizaciones
- [REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md) — Cheat sheet
- [ANALISIS_TECNICO.md](ANALISIS_TECNICO.md) — Análisis profundo

### Librerías Externas
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Python Official Docs](https://docs.python.org/3/)

---

## 🎯 Próximas Lecturas

Después de entender este programa, considera:
1. Estudiar **patrones de diseño** (MVC, Observer, etc.)
2. Aprender **testing unitario** con pytest
3. Explorar **async/await** para operaciones no bloqueantes
4. Investigar **build tools** (pyinstaller, wheel)
5. Estudiar **UI frameworks** más modernos (PyQt, Dear ImGui)

---

## 📞 Resumen Ejecutivo

**FastEditable** es una aplicación de escritorio **Tkinter** para procesar datos Excel/CSV.

**Arquitectura:**
- **Router** gestiona navegación entre pantallas
- **BaseScreen** proporciona plantilla para todas las pantallas
- **4 módulos funcionales** para operaciones diferentes
- **Sistema de estilos** centralizado para coherencia visual

**Stack:**
- Python 3.12+
- Tkinter (UI)
- Pandas (datos)

**Para empezar:**
```bash
python main.py
```

---

## 📝 Historial de Documentación

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 21 Apr 2026 | Documentación inicial completa |

---

**Autor:** FastEditable Team  
**Estado:** ✅ Documentación Completa  
**Última actualización:** 21 abril 2026

---

## Tabla de Referencia Rápida

```
┌─────────────────────────────────────────────────────────────────┐
│ 🎯 ENTRADA RÁPIDA A LA DOCUMENTACIÓN                            │
├─────────────────────────────────────────────────────────────────┤
│ ❓ ¿Quién soy?       → Lee MAPEO_PROGRAMA (Visión General)      │
│ ❓ ¿Cómo funciono?   → Lee ANALISIS_TECNICO                    │
│ ❓ ¿Cómo me modifico? → Lee REFERENCIA_RAPIDA                   │
│ ❓ ¿Tienes diagrama? → Lee DIAGRAMAS_VISUALES                   │
│ ❓ ¿Código específico? → Busca en ANALISIS_TECNICO              │
│ ❓ ¿Error?          → Consulta REFERENCIA_RAPIDA → Errores      │
│ ❓ ¿Color/Fuente?   → Consulta REFERENCIA_RAPIDA → Paleta       │
│ ❓ ¿Nuevo módulo?   → Lee REFERENCIA_RAPIDA → Checklist         │
└─────────────────────────────────────────────────────────────────┘
```

---

**¡Feliz lectura! 📚**
