import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly import graph_objects as go

DATA = '../data/Résultat_BMO_final2.csv'

@st.cache
def load_data():
    data = pd.read_csv(DATA)
    return data




data = load_data()

data = data.drop('Unnamed: 0', axis=1)
data = data.reset_index(drop=True)

with st.sidebar:
    job_to_filter = st.selectbox(
    'Choisissez un métier:',
    sorted(data['Métier'].unique()))
with st.sidebar:
    departement_to_filter =st.selectbox(
        'Choisissez un département:',
        sorted(data['Département'].unique()))


with st.sidebar:
    year_to_filter = st.slider('Année:', 2015, 2022, 2015)

filtered_data = data.loc[data['Année'] == year_to_filter]

job_data = filtered_data.loc[(filtered_data['Métier']==job_to_filter) & (filtered_data['Département']==departement_to_filter)]





col1, col2 = st.columns(2)
with col1:
    st.title("Besoins en Main d'Oeuvre {}".format(year_to_filter))
with col2:
    st.image('pole_emploi.png')

col1, col2 = st.columns(2)
with col1:
    st.header("Métier:")
    st.caption(job_to_filter)
with col2:
    st.header('Département:')
    st.caption(departement_to_filter)



classement = filtered_data.loc[filtered_data['Département']==departement_to_filter].sort_values(by='Projets de recrutement totaux', ascending=False).reset_index(drop=True)




with st.container():
    col0, col1, col2, col3 = st.columns(4)
    with col0:
        st.metric(label='CLASSEMENT', value=classement.loc[classement['Métier']==job_to_filter].index+1)
    with col1:
        if year_to_filter>2015:
            recrutement_total = job_data['Projets de recrutement totaux'].sum()
            recrutement_delta = int(recrutement_total - data.loc[(data['Année'] == year_to_filter-1) & (data['Métier']==job_to_filter) & (data['Département']==departement_to_filter)]['Projets de recrutement totaux'].sum())
            st.metric(label='TOTAL', value=recrutement_total, delta=recrutement_delta)
        else:
            recrutement_total = job_data['Projets de recrutement totaux'].sum()
            st.metric(label='TOTAL', value=recrutement_total, delta=0)

    with col2:
        if year_to_filter>2015:
            recrutement_total = job_data['Projets de recrutement difficiles'].sum()
            recrutement_delta = int(recrutement_total - data.loc[(data['Année'] == year_to_filter-1) & (data['Métier']==job_to_filter) & (data['Département']==departement_to_filter)]['Projets de recrutement difficiles'].sum())
            st.metric(label='DIFFICILE', value=recrutement_total, delta=recrutement_delta)
        else:
            recrutement_total = job_data['Projets de recrutement difficiles'].sum()
            st.metric(label='DIFFICILE', value=recrutement_total, delta=0)

    with col3:  
        if year_to_filter>2015:
            recrutement_total = job_data['Projets de recrutement saisonniers'].sum()
            recrutement_delta = int(recrutement_total - data.loc[(data['Année'] == year_to_filter-1) & (data['Métier']==job_to_filter) & (data['Département']==departement_to_filter)]['Projets de recrutement saisonniers'].sum())
            st.metric(label='SAISONNIER', value=recrutement_total, delta=recrutement_delta)
        else:
            recrutement_total = job_data['Projets de recrutement saisonniers'].sum()
            st.metric(label='SAISONNIER', value=recrutement_total, delta=0)
            
    st.caption("(Comparaison avec l'année {})".format(year_to_filter-1))
    
chart_data = data.loc[(data['Métier']==job_to_filter) & (data['Département']==departement_to_filter)]





st.subheader('Evolution des projets de recrutement:')



fig = px.line(
    chart_data,
    x='Année',
    y='Projets de recrutement totaux',
    hover_data=['Projets de recrutement totaux'],
    markers=False
   )

y_result = chart_data.loc[chart_data['Année']==year_to_filter]['Projets de recrutement totaux'].values

if len(y_result)>0:
    y_result = chart_data.loc[chart_data['Année']==year_to_filter]['Projets de recrutement totaux'].values[0]
else:
    y_result = 0
 
fig.add_trace(
    go.Scatter(
        x=[year_to_filter],
        y=[y_result],
        mode = 'markers',
        marker_symbol = 'star',
        marker_size = 15,
        name="Année sélectionnée"
    )
)



st.plotly_chart(fig, theme="streamlit", use_container_width=True)

st.subheader('Evolution des projets de recrutement difficiles:')



fig = px.line(
    chart_data,
    x='Année',
    y='Projets de recrutement difficiles',
    hover_data=['Projets de recrutement difficiles'],
    markers=False
   )

y_result = chart_data.loc[chart_data['Année']==year_to_filter]['Projets de recrutement difficiles'].values

if len(y_result)>0:
    y_result = chart_data.loc[chart_data['Année']==year_to_filter]['Projets de recrutement difficiles'].values[0]
else:
    y_result = 0

fig.add_trace(
    go.Scatter(
        x=[year_to_filter],
        y=[y_result],
        mode = 'markers',
        marker_symbol = 'star',
        marker_size = 15,
        name="Année sélectionnée"
    )
)

st.plotly_chart(fig, theme="streamlit", use_container_width=True)

st.subheader('Evolution des projets de recrutement saisonniers:')



fig = px.line(
    chart_data,
    x='Année',
    y='Projets de recrutement saisonniers',
    hover_data=['Projets de recrutement saisonniers'],
    markers=False
   )


y_result = chart_data.loc[chart_data['Année']==year_to_filter]['Projets de recrutement saisonniers'].values

if len(y_result)>0:
    y_result = chart_data.loc[chart_data['Année']==year_to_filter]['Projets de recrutement saisonniers'].values[0]
else:
    y_result = 0

fig.add_trace(
    go.Scatter(
        x=[year_to_filter],
        y=[y_result],
        mode = 'markers',
        marker_symbol = 'star',
        marker_size = 15,
        name="Année sélectionnée"
    )
)

st.plotly_chart(fig, theme="streamlit", use_container_width=True)

st.subheader('Classement des métiers {} :'.format(year_to_filter))


for index, metier in enumerate(classement['Métier']):
    st.caption(str(index+1)+" : "+metier)

#st.table(classement['Métier'])