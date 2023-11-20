import streamlit as st
import pandas as pd
from PIL import Image

st.title("Unegui.mn Laptop Listings Dashboard")

df = pd.read_csv('finaldf.csv', index_col=0)

st.dataframe(df)

st.sidebar.title('Filter Options')

price_range = st.sidebar.slider('Select Price Range', min_value=df['price'].min(), max_value=df['price'].max(), 
                                value=(df['price'].min(), df['price'].max()))
filtered_df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]

show_description = st.sidebar.checkbox('Show Description', value=False)

selection = st.sidebar.selectbox('Select a manufacturer', ('All', 'HP', 'Lenovo', 'Acer', 'Asus', 'Dell', 
                                                           'Apple', 'Gateway', 'other', 'MSI', 'Samsung',
                                                           'Evoo', 'Sony', 'Microsoft Surface'))

if selection == "All":
    filtered_df1 = filtered_df
else:
    filtered_df1 = filtered_df[filtered_df['manufacturer'] == selection]
    
    
if not show_description:
    st.dataframe(filtered_df1.drop('description', axis=1))
else:
    st.dataframe(filtered_df1)

