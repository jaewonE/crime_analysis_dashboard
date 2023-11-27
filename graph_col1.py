import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from uuid import uuid4

import folium
from streamlit_folium import folium_static
import plotly.express as px
import random


def create_plot(option, col):
    file = f'/Users/jaewone/Downloads/crime_analysis_dashboard/dataset/crime_by_office/경찰청_서울특별시지방경찰청_관서별 5대범죄 발생 및 검거 현황_{option}.csv'
    page_num = 0
    bar_per_page = 8

    df = pd.read_csv(file, encoding='cp949').dropna()
    df = df.groupby(['구분', '발생검거']).sum().reset_index()

    occ = df[df['발생검거'] == '발생']
    occ.sort_values(by='건수', ascending=False, inplace=True)
    office_list = occ.loc[:, '구분'].to_numpy()
    occ_list = occ.loc[:, '건수'].to_numpy()

    arrest = df[df['발생검거'] == '검거']
    arrest = arrest.set_index('구분').loc[office_list, :].reset_index()
    arrest_list = arrest.loc[:, '건수'].to_numpy()

    cur_index = page_num * bar_per_page
    show_office_list = office_list[cur_index: cur_index + bar_per_page]
    show_occ_list = occ_list[cur_index: cur_index + bar_per_page]
    show_arrest_list = arrest_list[cur_index: cur_index + bar_per_page]

    fig = plt.figure(figsize=(20, 8))
    bars1 = plt.bar(show_office_list, show_arrest_list, color='#ffd700')
    plt.bar(show_office_list, show_occ_list - show_arrest_list,
            color='#001f3f', bottom=show_arrest_list)
    plt.title('구별 범죄 발생 건수', fontsize=24)
    plt.xlabel('구분', fontsize=20)
    plt.ylabel('건수', fontsize=20)

    for i in range(len(bars1)):
        ratio = show_arrest_list[i] / show_occ_list[i] * 100
        plt.text(i, min(show_arrest_list[i], show_occ_list[i]) / 2,
                 f'{ratio:.1f}%', ha='center', color='black', fontweight=700, fontsize=18)

    plt.xticks(fontsize=20, weight="bold")
    plt.yticks(fontsize=20, weight="bold")
    plt.show()
    return fig


def show_graph1(layout):
    KEY = "graph1_key"
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
        st.markdown("### 경찰서별 검거율")

    fig = create_plot(option, layout)
    st.pyplot(fig)
