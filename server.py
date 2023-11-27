import matplotlib.pyplot as plt
import matplotlib.font_manager as fm  # 폰트 관련 용도 as fm
from map_graph.map_graph import show_map
from graphs.graph1 import graph1
from graphs.graph2 import graph2
from graphs.graph3 import graph3
from graphs.graph4 import graph4
import sys
import streamlit as st
import numpy as np
import os

sys.path.append('.')
st.set_page_config(layout="wide")


@st.cache_data
def fontRegistered():
    font_dirs = ['/Users/jaewone/Downloads/crime_analysis_dashboard/fonts']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:

        fm.fontManager.addfont(font_file)

    fm._load_fontmanager(try_read_cache=False)


def divider(width):
    return st.markdown(f"""<div style="height:1px;width:{width}px;border:none;color:#DEE1E6;background-color:#DEE1E6;" /> """, unsafe_allow_html=True)


fontRegistered()
plt.rc('font', family='NanumGothic')

st.markdown('# 서울시 범죄 현황 분석')
divider(1668)
left_layout, div, right_layout = st.columns([0.5, 0.01, 0.49])
st.markdown(
    """
    <style>
    [data-baseweb="select"] {
        margin-top: -20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with left_layout:
    graph1(figsize=(10, 4))
    divider(795)
    graph2(figsize=(10, 3))
    divider(795)
    graph3(figsize=(10, 5))

with div:
    st.markdown(f"""<div style="height:1330px;width:1px;border:none;color:#DEE1E6;background-color:#DEE1E6;" /> """,
                unsafe_allow_html=True)

with right_layout:
    show_map(right_layout, width=850, height=520)
    divider(850)
    graph4(width=850, height=580)
