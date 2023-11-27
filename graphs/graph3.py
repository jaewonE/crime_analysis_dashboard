import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from variable import *


def create_plot(option, figsize):
    guilty = option
    all_years_crime_location_data = []

    for year, file_path in zip(range(2016, 2022), area_file_list):
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
    fig = plt.figure(figsize=figsize)
    color_list = ['#000080', '#DC143C', '#228B22', '#FFD700',
                  '#4169E1', '#FF7F50', '#E6E6FA', '#40E0D0', '#FF69B4', '#808080']
    pivot_data.plot(kind='barh', stacked=True, color=color_list, ax=plt.gca())

    plt.title('연도별 서울시 범죄 발생 건수 상위 5개 장소')
    plt.xlabel('발생건수')
    plt.ylabel('년도')
    plt.xticks(rotation=45)
    plt.legend(title='장소', bbox_to_anchor=(1.05, 1))
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
    return fig


def graph3(figsize):
    KEY = "graph3_key"
    t1, t2 = st.columns([0.2, 0.8])
    with t1:
        option = st.selectbox(
            '',
            options=guilty_options,
            index=0,
            key=KEY,
        )

    with t2:
        st.markdown("### 범죄 유형별 발생 장소 Top5")

    fig = create_plot(option, figsize)
    st.pyplot(fig)
