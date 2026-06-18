import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Configuración de la página (Layout limpio y enfocado)
st.set_page_config(
    page_title="Seguimiento y Control - NOM-035",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilo personalizado para limitar colores y ruido visual
st.markdown("""
    <style>
    h1, h2, h3, p, span {
        font-family: 'Arial', sans-serif !important;
    }
    .kpi-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Encabezado del Dashboard Operativo Analítico (Orientado a Gerente de RRHH)
st.title("Monitoreo de factores de riesgo psicosocial (NOM-035)")
st.caption("Panel general para la supervisión de carga de trabajo y prevención de estrés")
st.markdown("---")

# --- GENERACIÓN DE DATOS SIMULADOS (MOCK DATA PARA EL PoC) ---
# Datos para Gráfico de Dispersión y Barras Horizontales
n_empleados = 20
np.random.seed(42)
datos_empleados = pd.DataFrame({
    'Empleado': [f'Empleado {i+1}' for i in range(n_empleados)],
    'Tareas directas (Superiores)': np.random.randint(2, 15, size=n_empleados),
    'Tareas aceptadas (Iniciativa propia)': np.random.randint(1, 10, size=n_empleados),
    'Área': np.random.choice(['Operaciones', 'Ventas', 'Finanzas', 'Tecnología'], size=n_empleados)
})

# Datos para Gráfico de Líneas
meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
ofertas_sin_asignar = [12, 19, 15, 28, 32, 45] # Tendencia al alza que alerta al usuario

# 3. DISEÑO DEL DASHBOARD (Distribución de Filas y Columnas)

# FILA 1: Componentes de control directo y alertas rápidas
col1, col2 = st.columns([2, 1])

with col1:
    # Componente 1: Monitoreo de Asignación Directa (Esquina superior izquierda - mayor captación visual)
    st.subheader("1. Carga de trabajo por asignación directa")
    st.markdown("<small>Identificación inmediata de cuellos de botella y posibles excesos de jornadas.</small>", unsafe_allow_html=True)

    # Gráfico de barras horizontales ordenadas de mayor a menor
    fig_bar = px.bar(
        datos_empleados.sort_values(by='Tareas directas (Superiores)'),
        x='Tareas directas (Superiores)',
        y='Empleado',
        orientation='h',
        color_discrete_sequence=['#1f77b4'],
        height=350
    )
    fig_bar.update_layout(margin=dict(l=20, r=20, t=10, b=20), yaxis_title=None)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    # Componente 2: Trabajo Pendiente por Asignación Diferida (Texto simple KPI)
    st.subheader("2. Pendientes diferidos")
    st.markdown("<small>Volumen acumulado por unidad organizacional a mitigar a futuro.</small>", unsafe_allow_html=True)

    st.markdown("""
        <div class='kpi-box'>
            <h3 style='margin:0; color:#1f77b4;'>14 Tareas</h3>
            <p style='margin:0; font-size:14px; color:#555;'>Sin asignar en el área de Operaciones</p>
        </div>
        <br>
        <div class='kpi-box'>
            <h3 style='margin:0; color:#1f77b4;'>8 Tareas</h3>
            <p style='margin:0; font-size:14px; color:#555;'>Sin asignar en el área de Ventas</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# FILA 2: Tendencias y Análisis de correlación (Equidad)
col3, col4 = st.columns([1, 1])

with col3:
    # Componente 3: Ofertas de Trabajo sin Asignar (Líneas por Área en el tiempo)
    st.subheader("3. Tendencia de ofertas rechazadas por área")
    st.markdown("<small>Seguimiento mensual para identificar departamentos con mayor resistencia o riesgo psicosocial.</small>", unsafe_allow_html=True)
    
    # NUEVOS DATOS SIMULADOS: Estructura en formato largo para múltiples líneas
    meses_lista = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'] * 4
    areas_lista = ['Operaciones']*6 + ['Ventas']*6 + ['Finanzas']*6 + ['Tecnología']*6
    
    # Tendencias simuladas (unas suben más que otras para la alerta visual)
    rechazos_lista = [
        10, 15, 12, 22, 28, 35,  # Operaciones (Hacia arriba)
        5,  7,  6,  8,  9,  11,  # Ventas (Estable)
        2,  3,  2,  4,  3,  5,   # Finanzas (Bajo)
        4,  6,  8,  9,  12, 14   # Tecnología (Moderado)
    ]
    
    df_tendencias = pd.DataFrame({
        'Mes': meses_lista,
        'Área': areas_lista,
        'Ofertas vacantes': rechazos_lista
    })
    
    # Gráfico de líneas multi-serie
    fig_line = px.line(
        df_tendencias,
        x='Mes', 
        y='Ofertas rechazadas',
        color='Área', # Esto crea una línea independiente por cada área
        color_discrete_sequence=['#1f77b4', '#aec7e8', '#ff7f0e', '#444444'], # Paleta limpia y consistente
        height=300
    )
    fig_line.update_traces(mode="lines+markers")
    fig_line.update_layout(
        margin=dict(l=20, r=20, t=10, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1) # Leyenda horizontal para ahorrar espacio
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col4:
    # Componente 4: Distribución Equitativa (Gráfico de dispersión para detectar excepciones)
    st.subheader("4. Correlación de equidad en la distribución")
    st.markdown("<small>Detección visual de empleados saturados frente a empleados subutilizados.</small>", unsafe_allow_html=True)

    fig_scatter = px.scatter(
        datos_empleados,
        x='Tareas aceptadas (Iniciativa propia)',
        y='Tareas directas (Superiores)',
        hover_name='Empleado',
        color='Área',
        color_discrete_sequence=['#1f77b4', '#aec7e8', '#ffbb78', '#444444'], 
        height=300
    )
    fig_scatter.update_layout(margin=dict(l=20, r=20, t=10, b=20))
    st.plotly_chart(fig_scatter, use_container_width=True)
