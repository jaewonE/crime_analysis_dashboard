import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from uuid import uuid4

import folium
from streamlit_folium import folium_static
import plotly.express as px
import random

def show_graph3(layout):
    t1, t2 = st.columns([0.2, 0.8])
    with t1:
        option = st.selectbox(
            '',
            (1, 2, 3, 4, 5),
            index=0,
            key=uuid4(),
            format_func=lambda x: f'Max: {x * 10}'
        )

    with t2:
        st.markdown("### Main Graph Title")

    # Sample data with 14 key-value pairs
    data = {
        'Category': [f'Key{i+1}' for i in range(14)],
        'Value': [random.randint(1, 100) for i in range(14)]
    }

    df = pd.DataFrame(data)

    # Custom color scale
    color_scale = [[0, '#76ACE0'], [1, '#94BFE9']]  # Starts with #6588B8 and fades to a lighter shade

    # Create a treemap
    fig = px.treemap(df, path=['Category'], values='Value',
                    color='Value', color_continuous_scale=color_scale,
                    custom_data=['Category', 'Value'], width=np.inf)

    # Update the layout and treemap labels
    fig.update_layout(
        plot_bgcolor='#fff',  # Set plot background to white
        paper_bgcolor='#fff',  # Set paper (area around the plot) background to white
        margin=dict(t=0, l=0, r=0, b=0),
    )

    fig.update_traces(
        texttemplate="<b>%{customdata[0]}</b><br>Value: %{customdata[1]}",
        textposition='middle center',
        hoverinfo='none'  # Disable hover info
    )

    # Streamlit commands
    st.plotly_chart(fig, use_container_width=True)