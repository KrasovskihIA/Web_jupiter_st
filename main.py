import pygwalker as pyg
from pygwalker.api.streamlit import StreamlitRenderer
import pandas as pd
import streamlit as st
import streamlit.components.v1 as stc
import os

# Функция для загрузки файлов
def load_data(data):
    # Словарь для месяцев
    month_mapping = {
        'Январь': 'January', 'Февраль': 'February', 'Март': 'March', 'Апрель': 'April',
        'Май': 'May', 'Июнь': 'June', 'Июль': 'July', 'Август': 'August',
        'Сентябрь': 'September', 'Октябрь': 'October', 'Ноябрь': 'November', 'Декабрь': 'December'
    }
    data_df = pd.read_csv(data, sep=',')

    data_df = data_df[data_df['Manufacture'] != '0']
    sales_by_manufacturer = data_df.groupby('Manufacture')['SALES_VOL'].sum().sort_values(ascending=False)
    top_10_manufacturers = sales_by_manufacturer.head(10).index
    data_df['Manufacture'] = data_df['Manufacture'].apply(lambda x: x if x in top_10_manufacturers else 'Прочие')

    data_df['Data'] = data_df['Data'].replace(month_mapping, regex=True)
    data_df['Data'] = pd.to_datetime(data_df['Data'], format='%B %Y')
    data_df = data_df.sort_values('Data')
    return data_df

def main():
    st.title("Use Pygwalker In Streamlit")
    menu = ['Home', 'About']
    choice = st.sidebar.selectbox('Menu', menu)
    if choice == 'Home':
        st.subheader('Home')
        with st.form('upload_form'):
            data_file = st.file_uploader('Upload a CSV file', type=['csv', 'txt'])
            submitted = st.form_submit_button('Submite')
        # Если есть какие то данные
        if submitted:
            df = load_data(data_file)
            # Визуализация
            return StreamlitRenderer(df, spec="./gw_config.json", spec_io_mode="rw")
    else:
        st.subheader('About')

if __name__ == '__main__':
    st.set_page_config(page_title="Use Pygwalker In Streamlit", layout="wide")
    renderer = main()
    if renderer:
        renderer.explorer()
