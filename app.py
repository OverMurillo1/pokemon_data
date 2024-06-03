import pandas as pd
import streamlit as st
import plotly.express as px

# Cargar datos
data = pd.read_csv('pokemon_data.csv', index_col='dexnum')

# Listas de opciones para los filtros
generaciones = ['Todos'] + data['generation'].unique().tolist()
tipos = ['Todos'] + data['type1'].unique().tolist()

# Título del dashboard
st.header('Dashboard Pokemon', divider='rainbow')

# Filtros en la barra lateral
with st.sidebar:
    st.subheader('Filtros', anchor=None,help=None, divider=True)
    generacion_filter = st.selectbox('Generacion', generaciones)
    tipo_filter = st.selectbox('Tipo', tipos)
    st.caption('Contacto')
    st.link_button('Linkedin','https://www.linkedin.com/in/jhampier-murillo-018270123/', use_container_width=True)
    

# Aplicar filtros
datos_filtrados = data.copy()
if generacion_filter != 'Todos':
    datos_filtrados = datos_filtrados[datos_filtrados['generation'] == generacion_filter]
if tipo_filter != 'Todos':
    datos_filtrados = datos_filtrados[datos_filtrados['type1'] == tipo_filter]
    
#Data Frame con todos los datos de los Pokémon
st.text('Dataframe con todos los datos de la base de Pokémon')
st.dataframe(datos_filtrados)
st.divider()

# Gráfico: Conteo de Pokémon por Tipo Principal
fig_hist = px.histogram(datos_filtrados, x='type1', title='Conteo de Pokemon por Tipo Principal', labels={'type1': 'Tipo Principal', 'count': 'Cantidad'})
fig_hist.update_layout(xaxis_tickangle=-90)
st.plotly_chart(fig_hist)
st.divider()

# Gráfico: Distribución de la Estadística de Ataque por Generación
fig_box = px.box(datos_filtrados, x='generation', y='attack', title='Distribución de la Estadística de Ataque por Generación', labels={'generation': 'Generación', 'attack': 'Ataque'}, category_orders={'generation': generaciones[1:]})
st.plotly_chart(fig_box)
st.divider()

# Gráfico: Comparación entre Pokémon Ordinarios y Legendarios
ordinary_group = datos_filtrados[datos_filtrados['special_group'] == 'Ordinary']
legendary_group = datos_filtrados[datos_filtrados['special_group'] == 'Legendary']
ordinary_stats = ordinary_group[['hp', 'attack', 'defense', 'speed', 'special_group']]
legendary_stats = legendary_group[['hp', 'attack', 'defense', 'speed', 'special_group']]
stats_union = pd.concat([ordinary_stats, legendary_stats])
stats_final = stats_union.melt(id_vars='special_group', var_name='Stats', value_name='Valores')
fig_comparison = px.box(stats_final, x='Stats', y='Valores', color='special_group', title='Comparación de Estadísticas entre Pokémon Ordinarios y Legendarios', labels={'Stats': 'Estadísticas', 'Valores': 'Valores', 'special_group': 'Grupo Especial'})
st.plotly_chart(fig_comparison)
st.divider()

# Gráfico: Matriz de Correlación entre las Estadísticas
pokemon_pair = datos_filtrados[['hp', 'attack', 'defense', 'speed', 'sp_atk', 'sp_def']]
corr = pokemon_pair.corr()
fig_corr = px.imshow(corr, labels=dict(color="Correlación"), x=pokemon_pair.columns, y=pokemon_pair.columns, title='Correlación de Estadísticas')
st.plotly_chart(fig_corr)
st.divider()

# Gráfico: Top 10 Pokémon más Grandes
height_top10 = datos_filtrados.groupby('name').agg({'height':'max'}).sort_values(by='height', ascending=False).head(10).reset_index()
fig_height = px.bar(height_top10, x='height', y='name', orientation='h', title='Top 10 Pokémon más Grandes (MTS)', labels={'height': 'Altura (MTS)', 'name': 'Nombre'})
st.plotly_chart(fig_height)
st.divider()

# Gráfico: Top 10 Pokémon más Pesados
weight_top10 = datos_filtrados.groupby('name').agg({'weight':'max'}).sort_values(by='weight', ascending=False).head(10).reset_index()
fig_weight = px.bar(weight_top10, x='weight', y='name', orientation='h', title='Top 10 Pokémon más Pesados (kg)', labels={'weight': 'Peso (kg)', 'name': 'Nombre'})
st.plotly_chart(fig_weight)
st.divider()

# Gráfico: Promedio de Estadísticas Base por Generación
generacion_hp = datos_filtrados.groupby('generation').agg({'hp':'mean', 'attack':'mean', 'defense':'mean', 'speed':'mean'}).reset_index()
generacion_hp_melt = pd.melt(generacion_hp, id_vars='generation', var_name='Stats', value_name='Promedio')
fig_promedio = px.line(generacion_hp_melt, x='generation', y='Promedio', color='Stats', title='Promedio de Estadísticas Base por Generación', labels={'generation': 'Generación', 'Promedio': 'Promedio', 'Stats': 'Estadísticas'})
st.plotly_chart(fig_promedio)
st.divider()

# Gráfico: Distribución de la Velocidad por Tipo
fig_speed = px.box(datos_filtrados, x='type1', y='speed', title='Distribución de la Velocidad por Tipo', labels={'type1': 'Tipo Principal', 'speed': 'Velocidad'}, category_orders={'type1': tipos[1:]})
st.plotly_chart(fig_speed)
st.divider()

# Gráfico: Promedio de Estadísticas Base por Tipo
stats_types = datos_filtrados.groupby('type1').agg({'hp':'mean', 'attack':'mean', 'defense':'mean', 'speed':'mean', 'sp_atk':'mean', 'sp_def':'mean'}).reset_index()
stats_types_melt = pd.melt(stats_types, id_vars='type1', var_name='Stats', value_name='Promedio')
fig_stats_type = px.bar(stats_types_melt, x='type1', y='Promedio', color='Stats', title='Promedio de Estadísticas Base por Tipo', labels={'type1': 'Tipo Principal', 'Promedio':'Promedio'})
st.plotly_chart(fig_stats_type)