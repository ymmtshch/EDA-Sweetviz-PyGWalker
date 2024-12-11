import pandas as pd
import pygwalker as pyg
import streamlit as st
import streamlit.components.v1 as components
import sweetviz as sv
import os
import tempfile

st.set_page_config(layout="wide")

# データを読み込む関数
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df

# SweetvizレポートをStreamlitで表示する関数
def st_display_sweetviz(report_html, height=1200):
    with open(report_html, 'r', encoding='utf8') as report_file:
        page = report_file.read()
    components.html(page, height=height, scrolling=True)

st.subheader("Data Analysis")
train_df = None
test_df = None

# タブを設定
tab_titles = ["pyGWalker", "sweet_viz"]
tabs = st.tabs(tab_titles)

# サイドバーでファイルをアップロード
with st.sidebar:
    uploaded_files = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_files is not None:
        train_df = load_data(uploaded_files)
    uploaded_compare = st.file_uploader("Choose a CSV file to compare (sweetviz only)", type=["csv"])
    if uploaded_compare is not None:
        test_df = load_data(uploaded_compare)

# pyGWalkerタブ
with tabs[0]:
    try:
        if train_df is not None:
            pyg_html = pyg.walk(train_df, return_html=True)
            components.html(pyg_html, height=1200, scrolling=True)
    except Exception as e:
        st.write(f"Error in pyGWalker: {e}")

# Sweetvizタブ
with tabs[1]:
    try:
        # 一時ディレクトリを利用
        target_path = tempfile.gettempdir()
        sv.config_parser.read_string("[General]\nuse_cjk_font=1")

        # 1つのCSV(train)データのみの場合
        if train_df is not None and test_df is None:
            out_file = os.path.join(target_path, "SWEETVIZ_REPORT.html")
            analysis = sv.analyze(train_df)
            analysis.show_html(filepath=out_file, open_browser=False, layout='vertical', scale=1.0)
            st_display_sweetviz(out_file)

        # 2つのCSV(trainとtest)データを比較する場合
        elif train_df is not None and test_df is not None:
            out_file = os.path.join(target_path, "SWEETVIZ_REPORT_COMPARE.html")
            analysis_com = sv.compare([train_df, "train"], [test_df, "test"])
            analysis_com.show_html(filepath=out_file, open_browser=False, layout='vertical', scale=1.0)
            st_display_sweetviz(out_file)
    except Exception as e:
        st.write(f"Error in Sweetviz: {e}")
