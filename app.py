import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import bar_chart_race as bcr
from datetime import datetime

def generate_data():
    np.random.seed(0)
    dates = pd.date_range(start="2018-01-01", end="2022-12-31", freq='ME')
    categories = ['Fiction', 'Non-fiction', 'Science', 'History', 'Children']
    data = {'Date': [], 'Category': [], 'Sales': []}
    for date in dates:
        for category in categories:
            data['Date'].append(date)
            data['Category'].append(category)
            data['Sales'].append(np.random.randint(100, 1000))
    return pd.DataFrame(data)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('book_sales_data.csv', parse_dates=['Date'])
    except FileNotFoundError:
        df = generate_data()
        df.to_csv('book_sales_data.csv', index=False)
    return df.copy()

df = load_data()
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.strftime('%Y-%m')
year = st.sidebar.selectbox('Select Year', sorted(df['Year'].unique()), index=4)
month = st.sidebar.selectbox('Select Month', sorted(df['Month'].unique()))
df_filtered_year = df[df['Year'] == year]
df_filtered_month = df[df['Month'] == month]
st.write("### Yearly Data")
fig, ax = plt.subplots()
df_filtered_year.groupby('Category')['Sales'].sum().plot(kind='bar', ax=ax)
st.pyplot(fig)
st.write("### Monthly Data")
fig, ax = plt.subplots()
df_filtered_month.groupby('Category')['Sales'].sum().plot(kind='bar', ax=ax)
st.pyplot(fig)

# Generate and embed bar chart race
df_pivot = df.pivot_table(index='Date', columns='Category', values='Sales', aggfunc='sum').cumsum()
file_path = 'bcr_race.html'
bcr.bar_chart_race(
    df=df_pivot,
    filename=file_path,
    orientation='h',
    sort='desc',
    n_bars=5,
    fixed_order=False,
    fixed_max=True,
    steps_per_period=10,
    interpolate_period=False,
    label_bars=True,
    bar_size=.95,
    period_label={'x': .99, 'y': .25, 'ha': 'right', 'va': 'center'},
    period_fmt='%B %d, %Y',
    dpi=144,
    cmap='dark24'
)

# Embed the HTML directly (consider security implications)
HtmlFile = open(file_path, 'r', encoding='utf-8')
source_code = HtmlFile.read()
st.markdown(source_code, unsafe_allow_html=True)
