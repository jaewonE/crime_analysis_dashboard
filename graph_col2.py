import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from uuid import uuid4
import os

import folium
from streamlit_folium import folium_static
import plotly.express as px
import random


def create_plot2(option, col):
    guilty = option

    data_all_years = []

    office_dataset_dir = '/Users/jaewone/Downloads/crime_analysis_dashboard/dataset/crime_by_office'
    file_paths = [os.path.join(office_dataset_dir, file)
                  for file in os.listdir(office_dataset_dir)]

    for year, file_path in zip(range(2016, 2022), file_paths):
        year_data = pd.read_csv(file_path, encoding='CP949')
        year_data['년도'] = year
        data_all_years.append(year_data)

    combined_data = pd.concat(data_all_years)
    relevant_columns = ['년도', '죄종', '발생검거', '건수']
    combined_data = combined_data[relevant_columns]

    # 죄종열에 있는 값 중 '강간,추행' 값은 '강간'으로 변경
    combined_data['죄종'] = combined_data['죄종'].replace('강간,추행', '강간')

    # 그룹화 및 합산
    grouped_data = combined_data.groupby(
        ['년도', '죄종', '발생검거']).sum().reset_index()
    occurrences = grouped_data[grouped_data['발생검거'] == '발생']
    occurrences = occurrences[occurrences['죄종'] == guilty]
    total_occurrences_per_year = occurrences.groupby('년도')['건수'].sum()

    # 그래프 그리기
    fig = plt.figure(figsize=(12, 6))
    plt.plot(total_occurrences_per_year.index, total_occurrences_per_year.values,
             marker='o', color='blue', label='발생 건수')
    plt.title('연도별 범죄 발생 건수 (서울시)')
    plt.xlabel('년도')
    plt.ylabel('건수')
    plt.legend()
    plt.grid(True)
    plt.show()
    return fig


def create_plot3(option, col):
    guilty = option
    all_years_crime_location_data = []

    area_dataset_dir = '/Users/jaewone/Downloads/crime_analysis_dashboard/dataset/crime_by_area'
    file_paths = [os.path.join(area_dataset_dir, file)
                  for file in os.listdir(area_dataset_dir)]

    for year, file_path in zip(range(2016, 2022), file_paths):
        year_data = pd.read_csv(file_path, encoding='CP949')
        year_data['년도'] = year
        all_years_crime_location_data.append(year_data)

    combined_crime_location_data = pd.concat(all_years_crime_location_data)

    # 데이터 그룹화 및 상위 5개 장소 선택
    combined_crime_location_data['범죄명'] = combined_crime_location_data['범죄명'].replace(
        '강간.추행', '강간')
    combined_crime_location_data = combined_crime_location_data[
        combined_crime_location_data['범죄명'] == guilty]
    grouped_data = combined_crime_location_data.groupby(
        ['년도', '장소'])['발생건수'].sum().reset_index()
    top_locations_by_year = grouped_data.groupby('년도').apply(
        lambda x: x.nlargest(6, '발생건수')).reset_index(drop=True)
    top_locations_by_year = top_locations_by_year.loc[top_locations_by_year['장소'] != '기타']

    # 데이터 재구조화
    pivot_data = top_locations_by_year.pivot(
        index='년도', columns='장소', values='발생건수').fillna(0)

    # 그래프 그리기
    fig = plt.figure(figsize=(15, 8))
    color_list = ['#000080', '#DC143C', '#228B22', '#FFD700',
                  '#4169E1', '#FF7F50', '#E6E6FA', '#40E0D0', '#FF69B4', '#808080']
    pivot_data.plot(kind='bar', stacked=True, color=color_list, ax=plt.gca())

    plt.title('연도별 서울시 범죄 발생 건수 상위 5개 장소')
    plt.xlabel('년도')
    plt.ylabel('발생건수')
    plt.xticks(rotation=45)
    plt.legend(title='장소', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
    return fig


def show_graph2(layout):
    guilty_list = ['살인', '강도', '강간', '절도', '폭력']

    t1, t2, t3, t4 = st.columns([0.2, 0.3, 0.2, 0.3])
    with t1:
        option1 = st.selectbox(
            '',
            options=guilty_list,
            index=0,
            key="graph2_key",
            # format_func=lambda x: f'{x}년'
        )
        print(f'option: {option1}')

    with t2:
        st.markdown("### 연도별 범죄 발생 건수")

    with t3:
        option2 = st.selectbox(
            '',
            options=guilty_list,
            index=0,
            key="graph3_key",
            # format_func=lambda x: f'{x}년'
        )
        print(f'option: {option2}')

    with t4:
        st.markdown("### 범죄 유형별 발생 장소 Top5")

    c1, c2 = layout.columns(2)

    with c1:
        fig = create_plot2(option1, c1)
        st.pyplot(fig)

    with c2:
        fig = create_plot3(option2, c2)
        st.pyplot(fig)
