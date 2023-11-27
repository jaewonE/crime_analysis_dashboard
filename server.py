import matplotlib.pyplot as plt
import matplotlib.font_manager as fm  # 폰트 관련 용도 as fm
from map_graph.map_graph import show_map
from graph_col3 import show_graph3
from graph_col2 import show_graph2
from graph_col1 import show_graph1
import sys
import streamlit as st
import numpy as np
import os
sys.path.append('.')


@st.cache_data
def fontRegistered():
    font_dirs = ['/Users/jaewone/Downloads/crime_analysis_dashboard/fonts']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:

        fm.fontManager.addfont(font_file)

    fm._load_fontmanager(try_read_cache=False)


st.set_page_config(layout="wide")

fontRegistered()
plt.rc('font', family='NanumGothic')

left_layout, right_layout = st.columns([0.6, 0.4])
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
    show_graph1(left_layout)
    show_graph2(left_layout)
    show_graph3(left_layout)

with right_layout:
    show_map(right_layout)
