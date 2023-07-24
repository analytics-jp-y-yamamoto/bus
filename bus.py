import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib

# ページのタイトル設定
st.set_page_config(
    page_title = "bus",
)

# csv読み込み
df0 = pd.read_csv('bass.csv', index_col = 0)

# セッション情報の初期化
if "page_id" not in st.session_state:
    st.session_state.page_id = -1
    st.session_state.df0 = df0

# 各種メニューの非表示設定
hide_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_style, unsafe_allow_html = True)


#選択する各項目のリスト作成用
def df_list(column):
    unique_list = st.session_state.df0[column].dropna(how='all').unique()
    st.session_state.df_list = unique_list

#選択されている項目のテキスト表示用
def add_text(selector, column):
    unique_list = st.session_state.df0[column].dropna(how='all').unique()
    sort_unique_list = np.sort(unique_list)
    selector = np.sort(selector)
    if np.array_equal(selector, sort_unique_list) == True:
        st.sidebar.text("全ての人が選ばれています。")
    else:
        st.sidebar.text(str(sort_unique_list).replace(str(selector),'') + "の人が除かれています。")

# 最初のページ
def main_page():
    st.markdown(
        "<h2 style='text-align: center;'>バス乗車数グラフ</h2>",
        unsafe_allow_html = True,
    )

    column_list = st.session_state.df0.columns.values
    column_list_selector = st.sidebar.selectbox("どの要素についてのグラフを描きますか？", column_list)

    #サイドバー作成用
    #生存or死亡
    df_list("時代")
    survive_selector = st.sidebar.multiselect("時代",st.session_state.df_list, default = st.session_state.df_list)
    if survive_selector == []:
        st.sidebar.text("どの時間も選ばれていません")
    elif survive_selector == [6]:
        st.sidebar.text("7時代が選ばれています。")
    elif survive_selector == [7]:
        st.sidebar.text("誰も選ばれていません")
    else:
        st.sidebar.text("全ての人が選ばれています。")

    #性別
    df_list("終点")
    sex_selector = st.sidebar.multiselect("終点", st.session_state.df_list, default = st.session_state.df_list)
    if sex_selector == ["Mセンター前"]:
        st.sidebar.text("Mセンター前が選ばれています。")
    elif sex_selector == ["Mセンター前"]:
        st.sidebar.text("女性が選ばれています。")
    elif sex_selector == []:
        st.sidebar.text("誰も選ばれていません")
    else:
        st.sidebar.text("全ての人が選ばれています。")

    st.session_state.select_arr = st.session_state.df0[
                                        (
                                        st.session_state.df0["時代"].isin(survive_selector)
                                        & st.session_state.df0["終点"].isin(sex_selector)
                                        )
                                    ][column_list_selector]
    count_arr = []
    count_select =[]
    column_arr = st.session_state.df0[column_list_selector]
    kind = list(set(column_arr.dropna(how='all')))

    for i in range(len(kind)):
        count_arr.append(list(column_arr).count(kind[i]))
        count_select.append(list(st.session_state.select_arr).count(kind[i]))

        fig, ax = plt.subplots()
        index = np.arange(len(kind))
        bar_width = 0.3

        ax.line_chart(index, count_arr, width = bar_width, label='ALL')
        ax.line_chart(index + bar_width, count_select, width = bar_width, label='select')
        ax.set_title(column_list_selector)
        ax.set_xticks(index + 0.5*bar_width, kind)
        ax.legend()

        st.pyplot(fig)

# ページ判定
if st.session_state.page_id == -1:
    main_page()
