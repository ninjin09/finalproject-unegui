import streamlit as st
import pandas as pd

st.title("Unegui.mn Laptop Listings Dashboard")

df = pd.read_csv('finaldf.csv')

st.sidebar.title('Filter Options')

price_range = st.sidebar.slider('Select Price Range', min_value=df['price'].min(), max_value=df['price'].max(), 
                                value=(df['price'].min(), df['price'].max()))

selection = st.sidebar.selectbox('select',("All", "HP", "Lenovo", "Acer", "Asus", "Dell", 
                                                           "Apple", "Gateway", "other", "MSI", "Samsung",
                                                           "Evoo", "Sony", "Microsoft Surface"))

if selection == "All":
    filtered_df = df
else:
    filtered_df = df[df['manufacturer'] == selection]

filtered_df1 = filtered_df[(filtered_df['price'] >= price_range[0]) & (filtered_df['price'] <= price_range[1])]

show_description = st.sidebar.checkbox('Show Description', value=False)

if not show_description:
    filtered_df2 = filtered_df1.drop('description', axis=1)
else:
    filtered_df2 = filtered_df1
    
show_nans = st.sidebar.checkbox('Hide Nan Values', value=False)
if show_nans:
    filtered_df3 = filtered_df2.dropna()
else:
    filtered_df3 = filtered_df2
    
st.dataframe(filtered_df3, width=3000)

st.write(f'## Bar Chart of Avg Price per Manufacturer')
avg_price_by_manufacturer = df.groupby('manufacturer')['price'].mean()
st.bar_chart(avg_price_by_manufacturer)

st.write(f'### Line Chart for Prices by Manufacturer')
for manufacturer, data in df.groupby('manufacturer'):
    st.write(manufacturer)
    st.line_chart(data['price'].reset_index(drop=True))
