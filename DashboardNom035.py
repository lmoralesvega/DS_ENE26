import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(
    page_title="Seguimiento NOM-035 - Gran Escala",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo UX/UI para limitar ruido visual y fuentes uniformes
st.markdown("""
    <style>
    h1, h2, h3, p, span, label {
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

# --- 2. GENERACIÓN DE DATOS SINTÉTICOS A GRAN ESCALA (5,000 REGISTROS) ---
@st.cache_data
def generar_datos_masivos():
    n_empleados = 5000
    np.random.seed(42)
    
    areas = ['Operaciones', 'Ventas', 'Finanzas', 'Tecnologia', 'Logistica', 'Recursos_Humanos']
    
    df = pd.DataFrame({
        'Empleado': [f'Emp-{i+1:04d}' for i in range(n_empleados)],
        'Area': np.random.choice(areas, size=n_empleados, p=[0.4, 0.2, 0.1, 0.15, 0.1, 0.05]),
        'Tareas_directas': np.random.randint(1, 18, size=n_empleados),
        'Tareas_aceptadas': np.random.randint(0, 12, size=n_empleados)
    })
    return df

df_total = generar_datos_masivos()

# --- 3. BARRA LATERAL DE FILTROS (CONTROL DE ESCALA) ---
st.sidebar.header("Filtros de Control")
st.sidebar.markdown("Use estos controles para reducir la carga visual del panel.")

listado_areas = ["Todas"] + list(df_total['Area'].unique())
area_seleccionada = st.sidebar.selectbox("Seleccionar Area Organizacional", listado_areas)

# Filtrado dinámico de la base de datos
if area_seleccionada == "Todas":
    df_filtrado = df_total
else:
    df_filtrado = df_total[df_total['Area'] == area_seleccionada]


# --- 4. DISEÑO DEL DASHBOARD ---
st.title("Monitoreo Organizacional - NOM-035")
st.caption(f"Visualizando escala masiva | Filtro activo: {area_seleccionada} ({len(df_filtrado)} empleados)")
st.markdown("---")

# FILA 1: CONTROL DIRECTO Y PENDIENTES
col1, col2 = st.columns([2, 1])

with col1:
    # Componente 1: Enfoque por Excepción (Top 15 más saturados)
    st.subheader("1. Casos criticos por asignacion directa (Top 15)")
    st.markdown("<small>Mostrando solo los empleados con mayor riesgo de sobrecarga para facilitar la intervencion.</small>", unsafe_allow_html=True)
    
    # Filtramos el Top 15 para evitar que el gráfico crezca infinitamente
    top_criticos = df_filtrado.sort_values(by='Tareas_directas', ascending=False).head(15)
    
    fig_bar = px.bar(
        top_criticos,
        x='Tareas_directas',
        y='Empleado',
        orientation='h',
        color_discrete_sequence=['#1f77b4'],
        height=450
    )
    fig_bar.update_layout(margin=dict(l=20, r=20, t=10, b=20), yaxis_title=None)
    fig_bar.update_yaxes(type='category', dtick=1)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    # Componente 2: KPIs agregados dinámicos
    st.subheader("2. Indicadores de Alerta")
    st.markdown("<small>Metricas calculadas en tiempo real segun el filtro seleccionado.</small>", unsafe_allow_html=True)
    
    # Calculamos alertas basadas en umbrales (ej. más de 14 tareas directas es riesgo)
    empleados_riesgo = len(df_filtrado[df_filtrado['Tareas_directas'] >= 14])
    promedio_tareas = df_filtrado['Tareas_directas'].mean()
    
    st.markdown(f"""
        <div class='kpi-box'>
            <h3 style='margin:0; color:#d62728;'>{empleados_riesgo} Empleados</h3>
            <p style='margin:0; font-size:14px; color:#555;'>En riesgo critico de burnout (NOM-035)</p>
        </div>
        <br>
        <div class='kpi-box'>
            <h3 style='margin:0; color:#1f77b4;'>{promedio_tareas:.1f} Tareas</h3>
            <p style='margin:0; font-size:14px; color:#555;'>Promedio de asignacion directa por persona</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# FILA 2: TENDENCIAS Y EQUIDAD
col3, col4 = st.columns([1, 1])

with col3:
    # Componente 3: Histórico de ofertas vacantes (Mantenemos la lógica de agregación mensual)
    st.subheader("3. Tendencia de ofertas rechazadas por area")
    st.markdown("<small>Volumen general de vacantes que nadie acepta (riesgo de clima laboral).</small>", unsafe_allow_html=True)
    
    meses_lista = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'] * 6
    areas_lista = ['Operaciones']*6 + ['Ventas']*6 + ['Finanzas']*6 + ['Tecnologia']*6 + ['Logistica']*6 + ['Recursos_Humanos']*6
    rechazos_lista = [
        10, 15, 12, 22, 28, 35,  # Operaciones
        5,  7,  6,  8,  9,  11,  # Ventas
        2,  3,  2,  4,  3,  5,   # Finanzas
        4,  6,  8,  9,  12, 14,  # Tecnologia
        8,  9,  11, 14, 13, 19,  # Logistica
        1,  2,  1,  1,  2,  3    # RRHH
    ]
    
    df_tendencias = pd.DataFrame({'Mes': meses_lista, 'Area': areas_lista, 'Ofertas_vacantes': rechazos_lista})
    
    # Si hay un área seleccionada, filtramos la línea del histórico también
    if area_seleccionada != "Todas":
        df_tendencias = df_tendencias[df_tendencias['Area'] == area_seleccionada]
        
    fig_line = px.line(
        df_tendencias, x='Mes', y='Ofertas_vacantes', color='Area',
        color_discrete_sequence=['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a'], height=300
    )
    fig_line.update_traces(mode="lines+markers")
    fig_line.update_layout(margin=dict(l=20, r=20, t=10, b=20), xaxis_title=None, yaxis_title="Ofertas vacantes")
    st.plotly_chart(fig_line, use_container_width=True)

with col4:
    # Componente 4: Mapa de calor de densidad para escala masiva
    st.subheader("4. Mapa de densidad de equidad distributiva")
    st.markdown("<small>Las zonas mas oscuras indican alta concentracion de empleados. Evite cuadrantes iluminados en la esquina superior izquierda (alta saturacion).</small>", unsafe_allow_html=True)
    
    fig_density = px.density_heatmap(
        df_filtrado,
        x='Tareas_aceptadas',
        y='Tareas_directas',
        nbinsx=15, # Define el tamaño de la cuadrícula en X
        nbinsy=15, # Define el tamaño de la cuadrícula en Y
        color_continuous_scale='Blues', # Mantiene tu paleta limitada y profesional
        height=300
    )
    
    fig_density.update_layout(
        margin=dict(l=20, r=20, t=10, b=20),
        xaxis_title="Tareas por iniciativa propia",
        yaxis_title="Tareas directas",
        coloraxis_showscale=True # Muestra la regla que dice cuántos empleados representa cada color
    )
    st.plotly_chart(fig_density, use_container_width=True)
