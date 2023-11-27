import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from uuid import uuid4

import folium
from streamlit_folium import folium_static
import random
import plotly.express as px
import os


def create_plot(option, col):
    file_path = f'/Users/jaewone/Downloads/crime_analysis_dashboard/dataset/crime_by_area/경찰청_서울특별시지방경찰청_범죄발생 장소별 현황_{option}.csv'
    crime_data = pd.read_csv(
        file_path, encoding='cp949').dropna().drop(columns='범죄명')
    crime_data = crime_data.groupby('장소').sum().reset_index()

    # Create a treemap
    fig = px.treemap(crime_data, path=[px.Constant(
        "연도에 따른 범죄 발생 장소"), '장소'], values='발생건수')
    fig.update_layout(width=1000, height=600)
    fig.update_traces(root_color="#F2DFCE")
    fig.update_layout(margin=dict(t=10, l=10, r=10, b=10))

    return fig


def show_graph3(layout):
    KEY = "graph5_key"
    t1, t2 = st.columns([0.2, 0.8])
    with t1:
        option = st.selectbox(
            '',
            options=[2016, 2017, 2018, 2019, 2020, 2021],
            index=0,
            key=KEY,
            format_func=lambda x: f'{x}년'
        )
        print(f'option: {option}')

    with t2:
        st.markdown("### 연도에 따른 범죄 발생 장소")

    fig = create_plot(option, layout)
    st.plotly_chart(fig)
