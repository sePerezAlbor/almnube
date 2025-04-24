import pandas as pd
import plotly.express as px
import streamlit as st
from pymongo import MongoClient

# --- Configuración de página ---
st.set_page_config(page_title='Dashboard Accidentalidad', layout='wide', page_icon=":dart:")
st.title('Dashboard de Accidentes en Barranquilla')

# --- Función para cargar datos con caché de 5 minutos ---
@st.cache_data(ttl=300)
def cargar_datos_desde_mongo():
    url = "mongodb+srv://perezalborsebastian:RHoAddewAZXIFILD@cluster0.klofmwq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&connectTimeoutMS=30000&socketTimeoutMS=30000"
    client = MongoClient(url)
    db = client['proyecto_personal']
    coleccion = db['Accidentedes_Barranquilla_victimas.csv']
    cursor = coleccion.find({}, {'_id': 0})
    return pd.DataFrame(cursor)

# --- Cargar datos ---
datos = cargar_datos_desde_mongo()
datos['Fecha_Accidente'] = pd.to_datetime(datos['Fecha_Accidente'], errors='coerce')
datos = datos.dropna(subset=['Fecha_Accidente'])
datos['anio'] = datos['Fecha_Accidente'].dt.year
datos['mes'] = datos['Fecha_Accidente'].dt.month
datos['mes_anio'] = datos['Fecha_Accidente'].dt.to_period('M').astype(str)

# --- Filtros por fecha ---
fechas_disponibles = sorted(datos['mes_anio'].unique())
st.sidebar.subheader("Rango de Fecha (Mes-Año)")
fecha_inicio = st.sidebar.selectbox("Fecha de inicio", fechas_disponibles, index=0)
fecha_fin = st.sidebar.selectbox("Fecha de fin", fechas_disponibles, index=len(fechas_disponibles)-1)
periodos = datos['Fecha_Accidente'].dt.to_period('M')
rango_inicio = pd.Period(fecha_inicio)
rango_fin = pd.Period(fecha_fin)
datos_filtrados = datos[(periodos >= rango_inicio) & (periodos <= rango_fin)]

# --- Diccionario de meses en español ---
diccionario_meses_espanol = {
    1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
    5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
    9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
}

# --- Gama cromática roja personalizada ---
colores_rojos = ['#800000', '#A52A2A', '#B22222', '#CD5C5C', '#DC143C', '#E9967A', '#FA8072']

# --- Indicadores ---
st.sidebar.metric("📊 Total de registros", len(datos))
st.sidebar.metric("📈 Registros filtrados", len(datos_filtrados))

# --- Gráfico 1: Ocurrencia de Accidentes por Mes ---
st.subheader("📆 Ocurrencia de Accidentes por Mes en Barranquilla")
ocurrencias_por_mes = datos_filtrados.groupby(pd.Grouper(key='Fecha_Accidente', freq='ME')).size().reset_index(name='Cantidad_Accidentes')
ocurrencias_por_mes['Numero_Mes'] = ocurrencias_por_mes['Fecha_Accidente'].dt.month
ocurrencias_por_mes['Año'] = ocurrencias_por_mes['Fecha_Accidente'].dt.year
ocurrencias_por_mes['Fecha_Tooltip'] = ocurrencias_por_mes.apply(lambda row: f"{diccionario_meses_espanol[row['Numero_Mes']]} de {row['Año']}", axis=1)

fig_tiempo = px.line(
    ocurrencias_por_mes, x='Fecha_Accidente', y='Cantidad_Accidentes',
    hover_data={'Fecha_Accidente': False, 'Fecha_Tooltip': True},
    labels={'Fecha_Accidente': 'Fecha', 'Cantidad_Accidentes': 'Número de Accidentes'}
)
fig_tiempo.update_traces(line_color='#B22222')
fig_tiempo.update_traces(hovertemplate="Mes: %{customdata[0]}<br>Número de Accidentes: %{y}<extra></extra>")
st.plotly_chart(fig_tiempo, use_container_width=True)

# --- Gráfico 2: Condición de la Víctima ---
st.subheader("⚠️ Condición de la Víctima")
df_condicion = datos_filtrados['CONDICION_VICTIMA'].value_counts().reset_index()
df_condicion.columns = ['CONDICION_VICTIMA', 'count']
fig_condicion = px.bar(df_condicion, x='CONDICION_VICTIMA', y='count', color='CONDICION_VICTIMA',
                       color_discrete_sequence=colores_rojos,
                       labels={'CONDICION_VICTIMA': 'Condición', 'count': 'Cantidad'})
st.plotly_chart(fig_condicion, use_container_width=True)

# --- Gráfico 3: Gravedad del Accidente ---
st.subheader("🚑 Gravedad del Accidente")
df_gravedad = datos_filtrados['GRAVEDAD_ACCIDENTE'].value_counts().reset_index()
df_gravedad.columns = ['GRAVEDAD_ACCIDENTE', 'count']
fig_gravedad = px.bar(df_gravedad, x='GRAVEDAD_ACCIDENTE', y='count', color='GRAVEDAD_ACCIDENTE',
                      color_discrete_sequence=colores_rojos,
                      labels={'GRAVEDAD_ACCIDENTE': 'Gravedad', 'count': 'Cantidad'})
st.plotly_chart(fig_gravedad, use_container_width=True)

# --- Gráfico 4: Clase de Accidente ---
st.subheader("🛑 Clase de Accidente")
df_clase = datos_filtrados['CLASE_ACCIDENTE'].value_counts().reset_index()
df_clase.columns = ['CLASE_ACCIDENTE', 'count']
fig_clase = px.bar(df_clase, x='CLASE_ACCIDENTE', y='count', color='CLASE_ACCIDENTE',
                   color_discrete_sequence=colores_rojos,
                   labels={'CLASE_ACCIDENTE': 'Clase', 'count': 'Cantidad'})
st.plotly_chart(fig_clase, use_container_width=True)

# --- Gráfico 5: Sexo de la Víctima (Pie Chart) ---
st.subheader("🚻 Distribución por Sexo de las Víctimas")
df_sexo = datos_filtrados['SEXO_VICTIMA'].value_counts().reset_index()
df_sexo.columns = ['SEXO_VICTIMA', 'count']
fig_sexo = px.pie(
    df_sexo,
    names='SEXO_VICTIMA',
    values='count',
    color_discrete_sequence=colores_rojos,
    hole=0.3,  # opcional: para un donut chart
    labels={'SEXO_VICTIMA': 'Sexo', 'count': 'Cantidad'}
)
fig_sexo.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_sexo, use_container_width=True)


# --- Gráfico 6: Histograma de Edad ---
st.subheader("📈 Distribución de Edad de las Víctimas")
datos_filtrados['EDAD_VICTIMA'] = pd.to_numeric(datos_filtrados['EDAD_VICTIMA'], errors='coerce')
fig_edad = px.histogram(datos_filtrados, x='EDAD_VICTIMA', nbins=30,
                        color_discrete_sequence=['#CD5C5C'],
                        labels={'EDAD_VICTIMA': 'Edad'})
st.plotly_chart(fig_edad, use_container_width=True)
