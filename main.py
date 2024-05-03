import pygwalker as pyg
from pygwalker.api.streamlit import StreamlitRenderer
from data_processing import load_data
import streamlit as st
import streamlit.components.v1 as stc
import os


def main():
    st.title("Use Pygwalker In Streamlit")
    menu = ['Home', 'About']
    choice = st.sidebar.selectbox('Menu', menu)
    if choice == 'Home':
        st.subheader('Home')
        with st.form('upload_form'):
            data_file = st.file_uploader('Upload a CSV file', type=['csv', 'txt'])
            submitted = st.form_submit_button('Submite')
        # Проверка на наличие данных и сохранение сессии
        if submitted and data_file is not None:
            df = load_data(data_file)
            st.session_state['df'] = df
            # Визуализация
            return StreamlitRenderer(df, spec="./gw_config.json", spec_io_mode="rw")
        if 'df' in st.session_state:
            return StreamlitRenderer(st.session_state['df'], spec="./gw_config.json", spec_io_mode="rw")
    else:
        st.subheader('About')

if __name__ == '__main__':
    st.set_page_config(page_title="Use Pygwalker In Streamlit", layout="wide")
    renderer = main()
    if renderer:
        renderer.explorer()
