import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

from variable import *


def create_plot(option, width, height):
    file_path = get_area_file(option)
    crime_data = pd.read_csv(
        file_path, encoding='cp949').dropna().drop(columns='범죄명')
    crime_data = crime_data.groupby('장소').sum().reset_index()

    # Create a treemap
    fig = px.treemap(crime_data, path=[px.Constant(
        "연도에 따른 범죄 발생 장소"), '장소'], values='발생건수')
    fig.update_layout(width=width, height=height)
    fig.update_traces(root_color="#F2DFCE")
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    # set text size
    fig.update_layout(font=dict(size=20))

    return fig


def graph4(width, height):
    KEY = "graph4_key"
    t1, t2 = st.columns([0.2, 0.8])
    with t1:
        option = st.selectbox(
            '',
            options=year_options,
            index=0,
            key=KEY,
            format_func=lambda x: f'{x}년'
        )
        print(f'option: {option}')

    with t2:
        st.markdown("### 연도에 따른 범죄 발생 장소")

    fig = create_plot(option, width, height)
    st.plotly_chart(fig)
