import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from variable import *


def create_plot(option, figsize):
    file = get_office_file(option)
    page_num = st.session_state['graph1_page_num']
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

    pages = len(office_list) // bar_per_page
    if len(office_list) % bar_per_page != 0:
        pages += 1
    st.session_state['graph1_max_page_num'] = pages
    print(f"pages: {st.session_state['graph1_max_page_num']}")

    cur_index = page_num * bar_per_page
    show_office_list = office_list[cur_index: cur_index + bar_per_page]
    show_occ_list = occ_list[cur_index: cur_index + bar_per_page]
    show_arrest_list = arrest_list[cur_index: cur_index + bar_per_page]

    fig = plt.figure(figsize=figsize)
    bars1 = plt.bar(show_office_list, show_arrest_list, color='#ffd700')
    bars2 = plt.bar(show_office_list, show_occ_list - show_arrest_list,
                    color='#001f3f', bottom=show_arrest_list)
    plt.title('구별 범죄 발생 건수', fontsize=20)
    plt.xlabel('구분', fontsize=12)
    plt.ylabel('건수', fontsize=12)

    plt.legend((bars1[0], bars2[0]), ('검거', '발생'),
               fontsize=10, loc='upper right')

    for i in range(len(bars1)):
        ratio = show_arrest_list[i] / show_occ_list[i] * 100
        plt.text(i, min(show_arrest_list[i], show_occ_list[i]) / 2,
                 f'{ratio:.1f}%', ha='center', color='black', fontweight=700, fontsize=14)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.show()
    return fig


def graph1(figsize):
    KEY = "graph1_key"
    if 'graph1_page_num' not in st.session_state:
        st.session_state['graph1_page_num'] = 0
    if 'graph1_max_page_num' not in st.session_state:
        st.session_state['graph1_max_page_num'] = 2
    t1, t2, left_btn, cur_page, right_btn, padding = st.columns(
        [0.2, 0.66, 0.04, 0.04, 0.04, 0.02])
    with t1:
        option = st.selectbox(
            '',
            options=year_options,
            index=0,
            key=KEY,
            format_func=lambda x: f'{x}년'
        )

    with t2:
        st.markdown("### 경찰서별 검거율")

    with left_btn:
        # add before and next button if is not first or last page
        if st.button('◀', key='before'):
            if st.session_state['graph1_page_num'] > 0:
                st.session_state['graph1_page_num'] -= 1
                print(f"cur page: {st.session_state['graph1_page_num']}")
                print(f'max page: {st.session_state["graph1_max_page_num"]}')
                st.experimental_rerun()

    with cur_page:
        # add current page number with fontSize 20px
        st.markdown(
            f"""<div style="font-size:20px;font-weight: semibold;padding-left:16px;padding-top:3px;">{st.session_state['graph1_page_num'] + 1}</div> """,
            unsafe_allow_html=True,
        )

    with right_btn:
        if st.button('▶', key='next'):
            if st.session_state['graph1_max_page_num'] - 1 > st.session_state['graph1_page_num']:
                st.session_state['graph1_page_num'] += 1
                print(f"cur page: {st.session_state['graph1_page_num']}")
                print(f'max page: {st.session_state["graph1_max_page_num"]}')
                st.experimental_rerun()

    with padding:
        # set width 10px div
        st.markdown(
            f"""<div style="height:1px;width:10px;border:none;" /> """,
            unsafe_allow_html=True,
        )

    fig = create_plot(option, figsize)
    st.pyplot(fig)
