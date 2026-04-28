# app/modules/normalizer.py
"""Módulo: Normalizar valores — detecta y unifica variantes de texto similares."""

import difflib
import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import unicodedata
import re

from app.ui import styles as s
from app.ui.components import (
    PrimaryBtn, SecondaryBtn, GhostBtn,
    Card, ScrollableFrame, Divider, Badge,
)
from app.ui.layouts import BaseScreen


def _norm_key(val: str) -> str:
    return val.strip().lower()


# ── CU: lista canónica de programas ──────────────────────────────────────────
_CANONICAL_PROGRAMS_CU = [
    "administración de la demanda y compras estratégicas",
    "administración de la empresa finanzas y gestión de negocios",
    "administración de operaciones y procesos de negocio herramientas claves de gestión",
    "administración logística y cadena de inventarios",
    "administración management aplicando scrum en equipos y otras metodologías de agilidad",
    "agile management aplicando scrum en equipos y otros metodos de agilidad organizacional",
    "agile management framework agile y scrum para equipos agiles",
    "analitica e inteligencia de negocios",
    "ai driven economics inteligencia artificial para analizar trafico y ventas",
    "analisis continuo de distribucion y planificacion estrategica",
    "analisis cuantitativo para la toma de decisiones",
    "analisis de datos con el uso de ia y big data",
    "analisis de datos inteligencia de negocios",
    "analisis de riesgos crediticios",
    "arquitectura de microservicios",
    "analisis y visualizacion de estados financieros a mediano y largo plazo",
    "analisis de datos con machine learning",
    "analitica empresarial con machine learning",
    "analitica web",
    "analitica y visualizacion con power bi y excel analitico",
    "aplicacion de metodologias agile en la gestion de proyectos",
    "arquitectura de centro de datos",
    "arquitectura de soluciones con tecnologias de la informacion",
    "auditoria de tecnologia de la informacion",
    "benchmarking de relaciones entorno mas practicos",
    "big data inteligencia artificial analisis para la practica",
    "bsc medicion e indicadores estrategicos de gestion",
    "buenas practicas para la obra",
    "buen gobierno compliance y gestion de riesgos empresariales",
    "business analytics para marketing enfoque aplicativo",
    "business intelligence",
    "business process management",
    "cambio climatico y negocio",
    "cadena de suministro y logistica",
    "chief technology officer cto",
    "coaching de equipos hacia la agilidad",
    "coaching ejecutivo herramienta estrategica para el alto desempeno",
    "coaching y modelo en equipo",
    "compliance y gobierno corporativo",
    "compliance auditoria operativa y financiera",
    "comunicacion asertiva",
    "comunicacion estrategica efectividad en la resolucion de conflictos y el trabajo en equipo",
    "comunicacion 30 generando valor un enfoque personal",
    "compras insight innovacion",
    "contabilidad financiera y general",
    "contabilidad de gestion",
    "control y contabilidad de costos",
    "contabilidad general y financiera avanzada",
    "contabilidad y finanzas para no especialistas",
    "content marketing influencer marketing",
    "control interno experiencia practica",
    "ciberseguridad y seguridad de la informacion",
    "costos y la gerencia",
    "costos y presupuestos",
    "creacion de nuevos productos y servicios",
    "crecimiento en relaciones entorno mas practicos",
    "customer experience gestion de la experiencia del cliente",
    "customer centric management",
    "customer journey management",
    "decisiones financieras de corto plazo",
    "design laboral",
    "desarrollo ejecutivo con por e inteligencia emocional",
    "data modeling para la innovacion",
    "design thinking innovar a traves del pensamiento creativo",
    "direccion de marketing y ventas blended strategy",
    "direccion estrategica del talento humano",
    "diseno de campanas multipagadoras online y offline",
    "diseno de estrategias de contenido para marketing digital",
    "diseno y gestion de procesos para la innovacion empresarial",
    "diseno analisis y valorizacion de puestos",
    "ecosistemas",
    "evaluacion financiera de proyectos y situaciones para la toma de decisiones",
    "evaluacion financiera de emprendimientos corporativos y estrategicas de crecimiento",
    "finanzas internacionales y cobertura cambiaria",
    "finanzas para la toma de decisiones gerenciales",
    "finanzas corporativas",
    "forecasting advanced planning and scheduling o optimizacion de la cadena de abastecimiento",
    "fundamentos de gestion de proyectos metodologias agil y tradicional para proyectos",
    "fundamentos de inteligencia artificial para los negocios",
    "fiscal avanzado",
    "gestion del cambio",
    "gerencia de compras y abastecimiento",
    "gestion de almacenes e inventarios avanzado",
    "gestion de almacenes aplicacion caso andaluzon",
    "gestion de arquitectura tecnologica de informacion",
    "gestion de compensaciones y beneficios",
    "gestion de costos de las tecnologias de informacion",
    "gestion de deuda y activos publicos",
    "gestion industrial basic",
    "gestion de la tesoreria",
    "gestion del conocimiento e innovacion thinking lean startup scrum",
    "gestion agil de proyectos de procesos para la era digital con product scrum kanban y design thinking",
    "gestion del deuda e ira digital",
    "gestion de marca y estrategia para startups y marketing empresas globales",
    "gestion de compensacion y beneficios y su impacto en las compras",
    "gestion de conflictos y soluciones",
    "gestion de equipos de alto desempeno",
    "gestion de equipos en entornos vuca y herramientas para empresas globales",
    "gestion de herramientas y eficacias y su impacto en las compras",
    "gestion de la cadena de suministros",
    "gestion de la compensacion implementando la ley de equidad salarial",
    "gestion de la innovacion con colaboracion",
    "gestion de la mejora continua",
    "gestion de la seguridad y proteccion de datos personales",
    "gestion de la sostenibilidad empresarial",
    "gestion de metricas para la innovacion",
    "gestion de infraestructura de ti",
    "gestion de proyectos agiles",
    "gestion de proyectos complejos",
    "gestion de proyectos con impacto estrategico",
    "gestion de proyectos de software",
    "gestion de recursos en proyectos",
    "gestion del cambio organizacional",
    "gestion de riesgos financieros",
    "gestion de riesgos en contratos",
    "gestion de riesgo empresarial y estrategico",
    "gestion de tesoreria",
    "gestion del cambio y adaptacion de la cultura organizacional",
    "gestion del capital de trabajo y flujo efectivo",
    "gestion financiera",
    "gestion estrategica con el uso de la metodologia kanban agile",
    "gestion de personas con base en indicadores de personas",
    "gestion del personal segun el codigo del trabajo",
    "gestion de proyectos agiles para empresas globales",
    "gestion de ti infraestructura",
    "gestion de ti y gestion de proyectos de ti",
    "gestion estrategica y gobernanza de datos",
    "growth hacking",
    "gestion logistica",
    "gestion logistica maritima",
    "gestion y coaching integrado el liderazgo la corporeidad y las emociones",
    "gestion y coaching integrado liderazgo o manejo",
    "gestion y marketing de la experiencia",
    "gestion y analisis de la informacion",
    "gestion y direccion de personas y talento",
    "growth hacking estrategias de crecimiento acelerado",
    "herramientas de analitica aplicadas a la gestion comercial",
    "herramientas de gestion y control para empresas globales",
    "herramientas para datos marketing",
    "herramientas financieras para dar informacion economica y auditoria de sostenibilidad en la empresa",
    "herramientas financieras para dar propuestas compradores",
    "herramientas para el analisis de datos",
    "herramientas para la gerencia de proyectos",
    "herramientas para la gestion de la innovacion",
    "herramientas tecnologicas para la gestion y comunicacion empresarial",
    "implementacion agil de procesos con design thinking y gobernando con scrum",
    "implementacion de herramientas de produccion y modelos para la trasposicion risk management",
    "indicadores de gestion financiera",
    "indicadores de gestion financieros",
    "innovacion creacion de valor para el negocio de procesos",
    "innovacion y diseno de servicios",
    "innovacion y gestion de la innovacion por inteligencia artificial",
    "innovacion y creacion de productos experimentados y su creacion de valor",
    "innovacion y creacion de propuestas a traves de la estrategia de la recuperacion",
    "inteligencia artificial",
    "inteligencia artificial para la gestion de proyectos",
    "inteligencia de mercado",
    "inteligencia emocional y liderazgo",
    "inteligencia emocional gestion de si mismo y la bolsa de valores",
    "inteligencia de negocios",
    "key account management",
    "liderazgo consciente y estrategico",
    "liderazgo y gestion de equipos",
    "la gestion del talento como palanca de la transformacion digital",
    "liderazgo de alto impacto",
    "liderazgo e inteligencia emocional",
    "liderazgo y coaching",
    "liderazgo y toma de decisiones",
    "lean management",
    "logistica y distribucion aplicada a finanzas",
    "marketing analytics 2 en 1 online offline decisiones basadas en datos",
    "marketing digital",
    "marketing de contenidos y plataformas digitales para estrategias empresariales",
    "marketing de servicios y experiencia del cliente",
    "marketing en linea seo social media y decisiones estrategicas",
    "marketing tecnologico",
    "metodologia del agile",
    "metodologia integral para la creacion y gestion de negocios business model canvas",
    "modelo de marketing",
    "modelo de negocio",
    "modelos y estrategias de agronegocios",
    "negociacion para ejecutivos de alta direccion",
    "inspeccion yo ventas de ventas en red nuevo b2b metricas y estrategias avanzadas",
    "negociacion y tecnicas de venta",
    "normas internacionales y tributacion",
    "optimizacion de alta ejecucion y financiero",
    "optimizacion de almacenes y distribucion",
    "optimizacion de la cadena de distribucion y financiero",
    "optimizacion de procesos con power bi y finanzas",
    "perspectivas de negocio con potencial e inteligencia artificial",
    "plan comercial efectivo",
    "planeamiento",
    "plan estrategico de marketing digital",
    "planeamiento estrategico",
    "planeamiento estrategico y control de la produccion",
    "planeamiento y gestion en organizaciones sin fines de lucro",
    "planeamiento financiero y analisis de variaciones con excel",
    "planificacion estrategica comercial para mercados competitivos",
    "planificacion estrategica aplicacion",
    "presentaciones efectivas del alto ejecutivo",
    "presentaciones efectivas de alto impacto",
    "product management",
    "project management avanzado",
    "propuesta estrategica diseno implementacion y control",
    "reclutamiento y seleccion",
    "relaciones y comunicacion de marketing digital",
    "retail management",
    "revenue management",
    "seguridad industrial",
    "sistema de costos abc",
    "smart digital marketing con ia",
    "storytelling para presentaciones efectivas",
    "supply chain management",
    "talento y organizacion claves del cambio",
    "tecnicas para calculos para alinear los datos incluyendo el ruido hacia el aprendizaje de maquina",
    "tecnologias emergentes cueva en el marketing",
    "tecnologias en ai marketing",
    "trade marketing para el retail",
    "tendencia de mercado",
    "transformacion de las instituciones del sector educacion hacia modelos con tecnologia e inteligencia artificial",
    "transformacion logistica al mundo digital",
    "transformacion digital basada en datos",
    "transformacion digital con experiencias innovadoras",
    "transformacion digital en organizaciones",
    "transformacion digital y los retos del profesional de sistemas",
    "transformacion digital y gobernanza de datos",
    "transforming rodearlo singletones y tendencias del cambia",
    "ui ux design metodologia de innovacion",
    "valorizacion de acciones y activos financieros para la toma de decisiones",
]

# Pre-computado al cargar el módulo — sin costo en tiempo de ejecución
_CANONICAL_CU_INDEX = {k: k for k in _CANONICAL_PROGRAMS_CU}


def _basic_normalize(val: str) -> str:
    """Transformación de texto pura: minúsculas, sin tildes ni caracteres especiales."""
    if not val or not isinstance(val, str):
        return ""

    FRASES_A_ELIMINAR = [
        r'\(online\)', r'\(presencial\)', r'\(ONLINE\)', r'\(PRESENCIAL\)',
        r'\(debe cambiarle el nombre\)',
        r'\(ok madre ti y colocarlo en administración tambien\)',
        r'\(ver profesor\)',
    ]
    PALABRAS_A_ELIMINAR = [r'\bG2\b', r'\bok\b']

    text = val.strip().lower()
    for frase in FRASES_A_ELIMINAR:
        text = re.sub(frase, '', text, flags=re.IGNORECASE)
    for palabra in PALABRAS_A_ELIMINAR:
        text = re.sub(palabra, '', text, flags=re.IGNORECASE)

    text = text.replace(':', '').replace(',', '').replace('.', '')
    text = text.replace('(', '').replace(')', '').replace('¿', '').replace('?', '')
    text = text.replace('&', '').replace('+', '').replace('-', ' ').replace('/', ' ')

    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = ' '.join(text.split())
    return text


def _normalize_programa_cu(val: str) -> str:
    """Normalización CU: transformación base + fuzzy match al diccionario canónico."""
    norm = _basic_normalize(val)
    if not norm:
        return ""
    if norm in _CANONICAL_CU_INDEX:
        return norm
    matches = difflib.get_close_matches(norm, _CANONICAL_PROGRAMS_CU, n=1, cutoff=0.82)
    return matches[0] if matches else norm


def _normalize_programa_c5(val: str) -> str:
    """Normalización C5 para columna Programa (por definir)."""
    if not val or not isinstance(val, str):
        return ""
    return _norm_key(val)


def _normalize_programa_re(val: str) -> str:
    """Normalización RE para columna Programa (por definir)."""
    if not val or not isinstance(val, str):
        return ""
    return _norm_key(val)


_PROGRAMA_NORMALIZERS = {
    "CU": _normalize_programa_cu,
    "C5": _normalize_programa_c5,
    "RE": _normalize_programa_re,
}


class NormalizerScreen(BaseScreen):
    title = "NORMALIZAR DATOS"

    def __init__(self, container, router):
        super().__init__(container, router)
        self.df: pd.DataFrame | None = None
        self._selected_col: str | None = None
        self._groups: dict = {}
        self._variant_vars: dict = {}
        self._norm_type: str = "CU"

    def _get_norm_key(self, val: str, col: str) -> str:
        if col.lower() == "programa":
            return _PROGRAMA_NORMALIZERS.get(self._norm_type, _norm_key)(val)
        return _norm_key(val)

    # ── shell ─────────────────────────────────────────────────────────────────
    def build_body(self, parent):
        action_bar = tk.Frame(parent, bg=s.C_BG, pady=10)
        action_bar.pack(fill="x", padx=s.PAD_LG)

        PrimaryBtn(action_bar, "Abrir archivo", command=self._load_file).pack(side="left")
        self._file_badge = Badge(action_bar, "Sin archivo cargado", kind="neutral")
        self._file_badge.pack(side="left", padx=10)

        self._btn_export = SecondaryBtn(action_bar, "Exportar resultado",
                                        command=self._export, state="disabled")
        self._btn_export.pack(side="right")

        # Selector de tipo: CU / C5 / RE
        type_frame = tk.Frame(action_bar, bg=s.C_BG)
        type_frame.pack(side="right", padx=(0, 16))
        tk.Label(type_frame, text="Tipo:", font=s.F_BTN_SM,
                 bg=s.C_BG, fg=s.C_GRAY).pack(side="left", padx=(0, 8))

        self._type_btns: dict = {}
        for t in ("CU", "C5", "RE"):
            btn = tk.Label(type_frame, text=t, font=s.F_BTN_SM,
                           padx=14, pady=5, cursor="hand2", relief="flat", bd=0)
            btn.pack(side="left", padx=2)
            self._type_btns[t] = btn
            btn.bind("<Button-1>", lambda e, nt=t: self._set_norm_type(nt))

        self._refresh_type_btns()

        Divider(parent).pack(fill="x")

        pane = tk.Frame(parent, bg=s.C_BG)
        pane.pack(fill="both", expand=True, padx=s.PAD_LG, pady=s.PAD_SM)

        p1 = tk.Frame(pane, bg=s.C_BG, width=175)
        p1.pack(side="left", fill="y", padx=(0, 10))
        p1.pack_propagate(False)
        self._build_columns_panel(p1)

        p2 = tk.Frame(pane, bg=s.C_BG, width=310)
        p2.pack(side="left", fill="y", padx=(0, 10))
        p2.pack_propagate(False)
        self._build_groups_panel(p2)

        p3 = tk.Frame(pane, bg=s.C_BG)
        p3.pack(side="left", fill="both", expand=True)
        self._build_editor_panel(p3)

    def _set_norm_type(self, norm_type: str):
        self._norm_type = norm_type
        self._refresh_type_btns()
        if self._selected_col and self.df is not None:
            self._analyze_column(self._selected_col)
            self._hide_editor()

    def _refresh_type_btns(self):
        for t, btn in self._type_btns.items():
            if t == self._norm_type:
                btn.config(bg=s.C_RED, fg="white")
            else:
                btn.config(bg=s.C_BG_CARD, fg=s.C_GRAY)

    # ── Panel 1: columnas ─────────────────────────────────────────────────────
    def _build_columns_panel(self, parent):
        tk.Label(parent, text="COLUMNAS", font=s.F_BTN_SM,
                 bg=s.C_BG, fg=s.C_GRAY_LT).pack(anchor="w", pady=(0, 6))

        outer = tk.Frame(parent, highlightbackground=s.C_BORDER,
                         highlightthickness=1, bg=s.C_BORDER)
        outer.pack(fill="both", expand=True)

        self._col_listbox = tk.Listbox(
            outer, bg=s.C_BG_CARD, bd=0, font=s.F_BODY,
            fg=s.C_DARK, selectbackground=s.C_RED_LT,
            selectforeground=s.C_RED, activestyle="none", relief="flat",
        )
        self._col_listbox.pack(fill="both", expand=True, padx=1, pady=1)
        self._col_listbox.bind("<<ListboxSelect>>", self._on_col_select)

    # ── Panel 2: grupos de variantes ──────────────────────────────────────────
    def _build_groups_panel(self, parent):
        hdr = tk.Frame(parent, bg=s.C_BG)
        hdr.pack(fill="x", pady=(0, 4))
        tk.Label(hdr, text="VALORES SIMILARES", font=s.F_BTN_SM,
                 bg=s.C_BG, fg=s.C_GRAY_LT).pack(side="left")
        self._groups_badge = Badge(hdr, "—", kind="neutral")
        self._groups_badge.pack(side="left", padx=6)

        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._refresh_groups_list())
        search_e = tk.Entry(parent, textvariable=self._search_var,
                            font=s.F_BODY, bg=s.C_BG_CARD,
                            relief="flat", highlightbackground=s.C_BORDER,
                            highlightthickness=1)
        search_e.pack(fill="x", ipady=5, pady=(0, 2))
        tk.Label(parent, text="Buscar en grupos...", font=s.F_SMALL,
                 bg=s.C_BG, fg=s.C_GRAY_LT).pack(anchor="w", pady=(0, 6))

        outer = tk.Frame(parent, highlightbackground=s.C_BORDER,
                         highlightthickness=1, bg=s.C_BORDER)
        outer.pack(fill="both", expand=True)
        self._groups_scroll = ScrollableFrame(outer, bg=s.C_BG_CARD)
        self._groups_scroll.pack(fill="both", expand=True, padx=1, pady=1)

    # ── Panel 3: editor ───────────────────────────────────────────────────────
    def _build_editor_panel(self, parent):
        editor_hdr = tk.Frame(parent, bg=s.C_BG)
        editor_hdr.pack(fill="x", pady=(0, 6))
        tk.Label(editor_hdr, text="EDITOR DE NORMALIZACIÓN", font=s.F_BTN_SM,
                 bg=s.C_BG, fg=s.C_GRAY_LT).pack(side="left")
        self._programs_count_badge = Badge(editor_hdr, "", kind="neutral")
        self._programs_count_badge.pack(side="left", padx=8)

        self._editor_card = Card(parent)
        self._editor_card.pack(fill="both", expand=True)

        # Placeholder
        self._placeholder = tk.Label(
            self._editor_card,
            text="← Selecciona un grupo de valores para editar",
            font=s.F_BODY, bg=s.C_BG_CARD, fg=s.C_GRAY_LT,
        )
        self._placeholder.pack(expand=True)

        # Editor inner (oculto inicialmente)
        self._editor_inner = tk.Frame(self._editor_card, bg=s.C_BG_CARD)

        # ── Sección superior: título y campo de reemplazo ──────────────────
        top = tk.Frame(self._editor_inner, bg=s.C_BG_CARD)
        top.pack(fill="x", padx=16, pady=(14, 0))

        self._group_title = tk.Label(
            top, text="", font=s.F_H1,
            bg=s.C_BG_CARD, fg=s.C_DARK, wraplength=420, justify="left",
        )
        self._group_title.pack(anchor="w", pady=(0, 4))

        self._group_info = Badge(top, "", kind="warn")
        self._group_info.pack(anchor="w", pady=(0, 10))

        Divider(top).pack(fill="x", pady=(0, 12))

        tk.Label(top, text="Normalizar a:",
                 font=s.F_BTN_SM, bg=s.C_BG_CARD, fg=s.C_GRAY).pack(anchor="w")
        self._replace_var = tk.StringVar()
        self._replace_entry = tk.Entry(
            top, textvariable=self._replace_var,
            font=("Segoe UI", 13), bg=s.C_BG,
            relief="flat", highlightbackground=s.C_RED, highlightthickness=2,
        )
        self._replace_entry.pack(fill="x", pady=(4, 0), ipady=7)

        # ── Botones de acción — packed side="bottom" antes del expand ──────
        # Esto garantiza que siempre sean visibles sin importar cuántas variantes haya
        btn_area = tk.Frame(self._editor_inner, bg=s.C_BG_CARD)
        btn_area.pack(side="bottom", fill="x", padx=16, pady=12)

        PrimaryBtn(btn_area, "Aplicar a seleccionadas",
                   command=self._apply_selected).pack(side="left")
        SecondaryBtn(btn_area, "Aplicar a todas las variantes",
                     command=self._apply_all).pack(side="left", padx=10)

        Divider(self._editor_inner).pack(side="bottom", fill="x")

        # ── Sección media: lista de variantes (expand rellena el resto) ────
        mid = tk.Frame(self._editor_inner, bg=s.C_BG_CARD)
        mid.pack(fill="both", expand=True, padx=16, pady=(12, 0))

        tk.Label(mid, text="Variantes encontradas — selecciona cuáles reemplazar:",
                 font=s.F_BTN_SM, bg=s.C_BG_CARD, fg=s.C_GRAY_LT).pack(anchor="w", pady=(0, 4))

        btn_row = tk.Frame(mid, bg=s.C_BG_CARD)
        btn_row.pack(fill="x", pady=(0, 6))
        GhostBtn(btn_row, "✓ Todas", command=self._select_all_variants).pack(side="left")
        GhostBtn(btn_row, "✗ Ninguna", command=self._deselect_all_variants).pack(side="left", padx=4)

        v_outer = tk.Frame(mid, bg=s.C_BG_CARD,
                           highlightbackground=s.C_BORDER, highlightthickness=1)
        v_outer.pack(fill="both", expand=True)
        self._variant_scroll = ScrollableFrame(v_outer, bg=s.C_BG_CARD)
        self._variant_scroll.pack(fill="both", expand=True, padx=1, pady=1)

    # ── Cargar archivo ────────────────────────────────────────────────────────
    def _load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Excel / CSV", "*.xlsx *.xlsm *.csv")])
        if not path:
            return
        try:
            if path.endswith(".csv"):
                df = pd.read_csv(path)
            else:
                xl = pd.ExcelFile(path)
                sheet = xl.sheet_names[0]
                if len(xl.sheet_names) > 1:
                    sheet = self._ask_sheet(xl.sheet_names) or sheet
                df = xl.parse(sheet)
        except Exception as e:
            messagebox.showerror("Error al cargar", str(e))
            return

        self.df = df.copy()
        fname = os.path.basename(path)
        self._file_badge.config(
            text=f"{fname}  ({len(df):,} filas × {len(df.columns)} cols)",
            fg=s.C_SUCCESS, bg="#E6F4ED")
        self.status.set(f"Cargado: {fname}", f"{len(df):,} filas")
        self._btn_export.config(state="normal")

        self._col_listbox.delete(0, tk.END)
        for col in df.columns:
            self._col_listbox.insert(tk.END, f"  {col}")
        self._selected_col = None
        self._groups.clear()
        self._clear_groups_list()
        self._hide_editor()

    def _ask_sheet(self, sheets):
        win = tk.Toplevel(self.container)
        win.title("Elegir hoja")
        win.grab_set()
        win.configure(bg=s.C_BG)
        win.geometry("300x300")
        tk.Label(win, text="¿Qué hoja deseas cargar?",
                 font=s.F_BODY, bg=s.C_BG, fg=s.C_DARK).pack(pady=10)
        lb = tk.Listbox(win, font=s.F_BODY, bg=s.C_BG_CARD, bd=0,
                        selectbackground=s.C_RED_LT, selectforeground=s.C_RED)
        lb.pack(fill="both", expand=True, padx=20, pady=6)
        for sh in sheets:
            lb.insert(tk.END, sh)
        lb.selection_set(0)
        result = [None]
        def ok():
            sel = lb.curselection()
            result[0] = sheets[sel[0]] if sel else sheets[0]
            win.destroy()
        PrimaryBtn(win, "Confirmar", command=ok).pack(pady=10)
        win.wait_window()
        return result[0]

    # ── Análisis de columna ───────────────────────────────────────────────────
    def _on_col_select(self, _event=None):
        idx = self._col_listbox.curselection()
        if not idx or self.df is None:
            return
        col = self.df.columns[idx[0]]
        self._selected_col = col
        self._analyze_column(col)
        self._hide_editor()

    def _analyze_column(self, col: str):
        series = self.df[col].dropna().astype(str)
        unique_count = series.nunique()
        self._programs_count_badge.config(
            text=f"{unique_count:,} programas únicos",
            fg=s.C_GRAY, bg=s.C_BG_CARD,
        )
        raw_groups: dict = {}

        for val in series:
            key = self._get_norm_key(val, col)
            raw_groups.setdefault(key, {})
            raw_groups[key][val] = raw_groups[key].get(val, 0) + 1

        self._groups = {
            k: {"variants": v, "total": sum(v.values())}
            for k, v in raw_groups.items()
            if len(v) > 1
        }
        self._refresh_groups_list()

    def _refresh_groups_list(self):
        for w in self._groups_scroll.inner.winfo_children():
            w.destroy()

        query = self._search_var.get().strip().lower()
        filtered = {
            k: v for k, v in self._groups.items()
            if not query or query in k
        }

        n = len(filtered)
        if n:
            self._groups_badge.config(text=f"{n} grupo(s)",
                                      fg=s.C_RED, bg=s.C_RED_LT)
        else:
            self._groups_badge.config(text="Sin variantes", fg=s.C_GRAY, bg=s.C_BG)

        if not filtered:
            msg = "Sin variantes encontradas" if self._selected_col else "Selecciona una columna"
            tk.Label(self._groups_scroll.inner, text=msg,
                     font=s.F_SMALL, bg=s.C_BG_CARD, fg=s.C_GRAY_LT).pack(pady=20)
            return

        for key, info in sorted(filtered.items()):
            self._make_group_row(key, info)

    def _make_group_row(self, key: str, info: dict):
        row = tk.Frame(self._groups_scroll.inner, bg=s.C_BG_CARD)
        row.pack(fill="x", pady=1, padx=2)

        card = tk.Frame(row, bg=s.C_BG_CARD,
                        highlightbackground=s.C_BORDER, highlightthickness=1,
                        cursor="hand2")
        card.pack(fill="x")

        top = tk.Frame(card, bg=s.C_BG_CARD, pady=7, padx=10, cursor="hand2")
        top.pack(fill="x")

        tk.Label(top, text=key, font=s.F_BODY, bg=s.C_BG_CARD,
                 fg=s.C_DARK, cursor="hand2", anchor="w").pack(side="left")
        Badge(top, f"{len(info['variants'])} var · {info['total']} filas",
              kind="warn").pack(side="right")

        preview_vals = list(info["variants"].keys())[:3]
        preview_text = "  →  " + "  |  ".join(f'"{v}"' for v in preview_vals)
        if len(info["variants"]) > 3:
            preview_text += f"  +{len(info['variants']) - 3} más"
        tk.Label(card, text=preview_text, font=s.F_SMALL,
                 bg=s.C_BG_CARD, fg=s.C_GRAY_LT,
                 anchor="w", cursor="hand2").pack(fill="x", padx=10, pady=(0, 6))

        def on_enter(e, c=card):
            c.config(highlightbackground=s.C_RED, highlightthickness=2)
        def on_leave(e, c=card):
            c.config(highlightbackground=s.C_BORDER, highlightthickness=1)
        def on_click(e, k=key, i=info):
            self._open_editor(k, i)

        for w in card.winfo_children() + [card]:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", on_click)
        for w in top.winfo_children():
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", on_click)

    # ── Editor ────────────────────────────────────────────────────────────────
    def _open_editor(self, key: str, info: dict):
        self._variant_vars.clear()

        best = max(info["variants"], key=info["variants"].get)

        if self._selected_col and self._selected_col.lower() == "programa":
            fn = _PROGRAMA_NORMALIZERS.get(self._norm_type, _norm_key)
            self._replace_var.set(fn(best))
        else:
            self._replace_var.set(best)

        self._group_title.config(text=f'"{key}"')
        self._group_info.config(
            text=f"{info['total']} ocurrencias · {len(info['variants'])} variantes distintas")

        for w in self._variant_scroll.inner.winfo_children():
            w.destroy()

        for variant, count in sorted(info["variants"].items(), key=lambda x: -x[1]):
            var = tk.BooleanVar(value=True)
            self._variant_vars[variant] = var

            row = tk.Frame(self._variant_scroll.inner, bg=s.C_BG_CARD)
            row.pack(fill="x", pady=3, padx=8)

            tk.Checkbutton(row, text=variant, variable=var,
                           font=s.F_BODY, bg=s.C_BG_CARD, fg=s.C_DARK,
                           activebackground=s.C_BG_CARD, selectcolor=s.C_RED_LT,
                           anchor="w").pack(side="left")
            Badge(row, f"{count} fila(s)", kind="neutral").pack(side="right")

        self._show_editor()

    def _show_editor(self):
        self._placeholder.pack_forget()
        self._editor_inner.pack(fill="both", expand=True)

    def _hide_editor(self):
        self._editor_inner.pack_forget()
        self._placeholder.pack(expand=True)

    def _select_all_variants(self):
        for v in self._variant_vars.values():
            v.set(True)

    def _deselect_all_variants(self):
        for v in self._variant_vars.values():
            v.set(False)

    # ── Aplicar reemplazo ─────────────────────────────────────────────────────
    def _apply_selected(self):
        selected = [v for v, var in self._variant_vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("Atención", "Selecciona al menos una variante.")
            return
        self._do_replace(selected)

    def _apply_all(self):
        self._do_replace(list(self._variant_vars.keys()))

    def _do_replace(self, variants: list[str]):
        if not variants or self._selected_col is None or self.df is None:
            return
        new_val = self._replace_var.get()
        if not new_val.strip():
            messagebox.showwarning("Atención", "Escribe el valor de reemplazo.")
            return

        col = self._selected_col
        mask = self.df[col].astype(str).isin(variants)
        n_changed = int(mask.sum())
        self.df.loc[mask, col] = new_val

        self._analyze_column(col)
        self._hide_editor()
        self.status.set(f"{n_changed} celdas actualizadas en '{col}'.",
                        f"→ \"{new_val}\"")
        messagebox.showinfo("Aplicado",
                            f"✓ {n_changed} celda(s) reemplazadas por \"{new_val}\"")

    # ── Limpiar ───────────────────────────────────────────────────────────────
    def _clear_groups_list(self):
        for w in self._groups_scroll.inner.winfo_children():
            w.destroy()
        self._groups_badge.config(text="—", fg=s.C_GRAY, bg=s.C_BG)

    # ── Exportar ──────────────────────────────────────────────────────────────
    def _export(self):
        if self.df is None:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv")],
        )
        if not path:
            return
        try:
            if path.endswith(".csv"):
                self.df.to_csv(path, index=False)
            else:
                self.df.to_excel(path, index=False)
            messagebox.showinfo("Exportado",
                                f"✓ {len(self.df):,} filas guardadas en:\n{path}")
            self.status.set("Exportación completada.", f"{len(self.df):,} filas")
        except Exception as e:
            messagebox.showerror("Error al exportar", str(e))
