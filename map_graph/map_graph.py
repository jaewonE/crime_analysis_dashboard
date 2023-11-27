import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from uuid import uuid4

import folium
from streamlit_folium import folium_static
import plotly.express as px
import random
import os

main_dir = os.path.join(os.getcwd().split("crime_analysis_dashboard")[0], 'crime_analysis_dashboard')
csv_dir = os.path.join(main_dir, 'dataset', 'crime_by_office')
json_dir = os.path.join(main_dir, 'map_graph', 'cache')
csv_prefix = "경찰청_서울특별시지방경찰청_관서별 5대범죄 발생 및 검거 현황"

office_location_path = os.path.join(main_dir, 'map_graph', 'office_location.csv')
geojson_path = os.path.join(main_dir, 'dataset', 'seoul_municipalities_geo_simple.json')


def get_crime_data(year):
    json_path = os.path.join(json_dir, f'{year}.json')
    if os.path.exists(json_path):
        return pd.read_json(json_path, orient='index').to_dict()[0]

    df = pd.read_csv(os.path.join(csv_dir,
                     f'{csv_prefix}_{year}.csv'), encoding='cp949')
    df = df[df['발생검거'] == '발생']
    act_count = df[['구분', '건수']].groupby('구분').sum()
    act_count['건수'].to_json(path_or_buf=json_path, force_ascii=False)
    return act_count.astype(np.int64).to_dict()['건수']


def show_map(layout):
    KEY = "map_graph_key"
    location_df = pd.read_csv(office_location_path).set_index('office')

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
        st.markdown("### 경찰 행정 구역에 따른 범죄 발생 건수")

    # Create a map centered around Seoul
    seoul_map = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

    folium.GeoJson(
        geojson_path,
        name='Seoul Boundary',
        style_function=lambda x: {
            'color': '#D3BCD9',  # Light blue color
            'weight': 2,         # Thinner line
            'fillOpacity': 0.35   # Lower fill opacity
        }
    ).add_to(seoul_map)

    # Add crime occurrences as circles with bold numbers
    crime_data = get_crime_data(option)
    for station, count in crime_data.items():
        _, lat, lon = location_df.loc[station]
        location = (lat, lon)
        folium.CircleMarker(
            location=location,
            radius=count * 0.000001 * count,  # Adjust the radius as needed
            color=None,  # No border
            fill=True,
            fill_color='#6FA3CC',
            fill_opacity=0.8,
            tooltip=f'{station}: {count}건'
        ).add_to(seoul_map)
        # Calculate offset for text to be in the center of the circle
        offset_x = -10
        offset_y = 5

        folium.map.Marker(
            location,
            icon=folium.DivIcon(
                html=f'<div style="position: relative; bottom: {offset_y}px; left: {offset_x}px; font-size: 11pt; color: black; font-weight: bold;">{"" if count < 4000 else count}</div>'
            )
        ).add_to(seoul_map)

    # Display the map in Streamlit
    # st.markdown(
    #     """<div style = "height: 30px;" />""",
    #     unsafe_allow_html=True,
    # )
    folium_static(seoul_map, height=250*3)