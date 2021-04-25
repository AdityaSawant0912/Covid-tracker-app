# Python 3.9
# Aditya Sawant
# hola

import streamlit as st
import numpy as np
import pandas as pd
import requests
from plotly.offline import iplot
import plotly.graph_objs as go
import plotly.express as px
from pandas.io.json import json_normalize

# from streamlit.ScriptRunner import StopException, RerunException

fig = go.Figure()
st.write("""
# Covid19 Tracking App 🚑
[Coronavirus COVID19 API](https://documenter.getpostman.com/view/10808728/SzS8rjbc?version=latest#81447902-b68a-4e79-9df9-1b371905e9fa) is used to get the data in this app.
""")

st.write(
    'Coronavirus is officially a pandemic. Since the first case in december the disease has spread fast reaching almost every corner of the world.' +
    'They said it\'s not a severe disease but the number of people that needs hospital care is growing as fast as the new cases.' +
    'Some governments are taking measures to prevent a sanitary collapse to be able to take care of all these people.' +
    'I\'m tackling this challenge here. Let\'s see how some countries/regions are doing!')

url = 'https://api.covid19api.com/countries'
r = requests.get(url)
df0 = json_normalize(r.json())

top_row = pd.DataFrame({'Country': ['Select a Country'], 'Slug': ['Empty'], 'ISO2': ['E']})

df0 = pd.concat([top_row, df0]).reset_index(drop=True)

# Side bar

st.sidebar.header('Create/Filter your search')
graph_type = st.sidebar.selectbox('Cases', ('confirmed', 'deaths', 'recovered'))
st.sidebar.subheader('Search by Country')
country = st.sidebar.selectbox('Country', df0.Country)

country1 = st.sidebar.selectbox('Compare with another Country', df0.Country)
if st.sidebar.button('Refresh Data'):
    raise st._RerunException(st._RerunData(None))

if country != 'Select a Country':
    slug = df0.Slug[df0['Country'] == country].to_string(index=False)
    st.write(slug)
    url = 'https://api.covid19api.com/total/dayone/country/' + slug + '/status/' + graph_type
    r = requests.get(url)
    st.write("""# Total """ + graph_type + """ cases in """ + country + """ are: """ + str(r.json()[-1].get("Cases")))
    df = json_normalize(r.json())
    layout = go.Layout(
        title=country + '\'s '  + graph_type + ' cases Date',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Number of Cases'),
    )
    fig.update_layout(dict1=layout, overwrite=True)
    fig.add_trace(go.Scatter(x=df.Date, y=df.Cases, mode='lines', name=country))
    st.write("")

    if country1 != 'Select a Country':
        slug1 = df0.Slug[df0['Country'] == country1].to_string(index=False)
        url = 'https://api.covid19api.com/total/dayone/country/' + slug1 + '/status/' + graph_type
        r = requests.get(url)
        # st.write(str(r.json()))
        if str(r.json()) == "{'message': 'for performance reasons, please specify a province'}"or str(r.json()) == '[]':
            st.write("")
            st.write(f"""Couldn't show cases of {country1} due to technical issues""")
            st.write("")
        else:
            st.write("""# Total """ + graph_type + """ cases in """ + country1 + """ are: """ + str(r.json()[-1].get("Cases")))
            df = json_normalize(r.json())
            layout = go.Layout(
                title=country + ' vs ' + country1 + ' ' + graph_type + ' cases Data',
                xaxis=dict(title='Date'),
                yaxis=dict(title='Number of cases'), )
            fig.update_layout(dict1=layout, overwrite=True)
            fig.add_trace(go.Scatter(x=df.Date, y=df.Cases, mode='lines', name=country1))
            st.write("")

    st.plotly_chart(fig, use_container_width=True)


else:
    url = 'https://api.covid19api.com/world/total'
    r = requests.get(url)
    total = r.json()["TotalConfirmed"]
    deaths = r.json()["TotalDeaths"]
    recovered = r.json()["TotalRecovered"]
    st.write("""# Worldwide Data:""")
    st.write("Total cases: " + str(total) + ", Total deaths: " + str(deaths) + ", Total recovered: " + str(recovered))
    x = ["TotalConfirmed", "TotalDeath", "TotalRecovered"]
    y = [total, deaths, recovered]

    layout = go.Layout(
        title='World Data',
        xaxis=dict(title='Category'),
        yaxis=dict(title='Number of cases'),
    )

    fig.update_layout(dict1=layout, overwrite=True)
    fig.add_trace(go.Bar(name='World Data', x=x, y=y))
    st.plotly_chart(fig, use_container_width=True)