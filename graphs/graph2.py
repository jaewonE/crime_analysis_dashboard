import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from variable import *


def create_plot(option, figsize):
    guilty = option

    data_all_years = []

    for year, file_path in zip(range(2016, 2022), office_file_list):
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
    fig = plt.figure(figsize=figsize)
    plt.plot(total_occurrences_per_year.index, total_occurrences_per_year.values,
             marker='o', color='blue', label='발생 건수')
    plt.title('연도별 범죄 발생 건수 (서울시)')
    plt.xlabel('년도')
    plt.ylabel('건수')
    plt.legend()
    plt.grid(True)
    plt.show()
    return fig


def graph2(figsize):
    KEY = "graph2_key"
    t1, t2 = st.columns([0.2, 0.8])
    with t1:
        option = st.selectbox(
            '',
            options=guilty_options,
            index=0,
            key=KEY,
        )

    with t2:
        st.markdown("### 연도별 범죄 발생 건수")

    fig = create_plot(option, figsize)
    st.pyplot(fig)
