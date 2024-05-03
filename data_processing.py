import pandas as pd
import streamlit as st


# Функция для загрузки файлов
@st.cache_data
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