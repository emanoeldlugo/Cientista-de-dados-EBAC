import streamlit as st
import pandas as pd
import numpy as np
import requests

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
data_load_state.text("Done! (using st.cache_data)")
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

st.subheader('Number of pickups by hour')

hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)

hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)


def load_data(url):
    df = pd.read_csv(url)  # 👈 Download the data
    return df

df = load_data("https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")
st.dataframe(df)

st.button("Rerun")

def api_call():
    response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    return response.json()

from st_aggrid import AgGrid, GridOptionsBuilder

# Cria um DataFrame de exemplo

df = pd.read_csv('base_sinasc_RO_2019.csv')

st.title("Pivot Table no Streamlit")

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
gb.configure_side_bar()  # Habilita a barra lateral para configuração
grid_options = gb.build()

AgGrid(
    df,
    gridOptions=grid_options,
    enable_enterprise_modules=True,
    update_mode='MODEL_CHANGED',
    fit_columns_on_grid_load=True
)

st.write("Use a barra lateral para configurar a tabela dinâmica. Arraste as colunas para 'Row Groups', 'Values', e 'Columns' para criar pivôs.")

st.image('bandeira.png')

with st.form(key='my_form'):
    username = st.text_input('Username')
    password = st.text_input('Password')
    st.form_submit_button('Login')

st.button('Hit me')

st.text_input('Enter some text')

st.number_input('Enter a number')

st.text_area('Area for textual entry')

st.date_input('Date input')

st.time_input('Time entry')

st.file_uploader('File uploader')