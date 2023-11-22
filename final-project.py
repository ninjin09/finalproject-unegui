import streamlit as st
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

st.title("Unegui.mn Laptop Listings Dashboard")

if st.button('Refresh the Data!'):
#############################################################################################################
    urls = []
    condition = []
    description = []
    manufacturer = []
    price = []
    screen = []
    gpu = []
    storage = []
    ram = []
    processor = []
    storage_sizes = ['128GB', '256GB', '512GB', '1TB', '2TB', '4TB', '8TB', '128 GB', '256 GB', '512 GB', '1 TB', '2 TB', '4 TB', '8 TB']
    ram_sizes = ['4GB', '8GB', '16GB', '32GB', '64GB', '4 GB', '8 GB', '16 GB', '32 GB', '64 GB']
    processors = ['i3','i5', 'i7', 'i9', 'M2', 'M1', 'M3', 'Ryzen5', 'Ryzen5', 'Ryzen7', 'Ryzen9', 'Ryzen 9', 'Ryzen 7', 'Ryzen 5', 'Ryzen 3', 'Celeron']
    graphics_cards = ['GTX 1650', 'GTX 1660', 'RTX 2060', 'RTX 2070', 'RTX 2080', 'RTX 2070', 'RTX 2070', 'RTX 2080', 'RTX 3050', 
                     'RTX 3050 Ti', 'RTX 3060', 'RTX 3070', 'RTX 3080 Ti', 'RTX 3080', 'AMD Radeon', 'Radeon AMD', 'Intel UHD', 'Apple']
#############################################################################################################
    i = 1
    while i<=1:
        url = f"https://www.unegui.mn/kompyuter-busad/notebook/?page={i}&condition=new"
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
        links = soup.find_all("a",{"class":"mask"})
        for link in links:
            url = link.get('href')
            full_url = "https://www.unegui.mn/" + url
            urls.append(full_url)
            condition.append("New")
        i = i + 1
    #gathering used listing links
    i = 1
    while i<=1:
        url = f"https://www.unegui.mn/kompyuter-busad/notebook/?page={i}&condition=used"
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
        links = soup.find_all("a",{"class":"mask"})
        for link in links:
            url = link.get('href')
            full_url = "https://www.unegui.mn/" + url
            urls.append(full_url)
            condition.append("Used")
        i = i + 1
    #scraping price, manufacturer, price and screen size
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
        page_content = soup.find_all("div",{"class":"js-description"})
        description.append(page_content[0].get_text().replace('\n',' '))

        price0 = soup.find("div",{"class":"announcement-price__cost"}).get_text(strip=True).split(" ")
        price.append(price0[0])

        manufacturer0 = soup.find_all("span",{"itemprop":"name"})
        manufacturer.append(manufacturer0[3].get_text())

        screen0 = soup.find_all("a",{"class":"value-chars"})
        screen.append(screen0[0].get_text(strip=True))
        
    for i in range(len(graphics_cards)):
        graphics_card = graphics_cards[i].replace(' ','')
        graphics_cards.append(graphics_card)

    cpu_pattern = re.compile(r'CPU: ([^\-]+)')
    ram_pattern = re.compile(r'RAM: ([^\-]+)')
    storage_pattern = re.compile(r'HARD: ([^\-]+)')
    display_pattern = re.compile(r'Display: ([^\-]+)')

    graphics_card_pattern = re.compile(fr'\b({"|".join(map(re.escape, graphics_cards))})\b', flags=re.IGNORECASE)
    storage_size_pattern = re.compile(fr'\b({"|".join(map(re.escape, storage_sizes))})\b', flags=re.IGNORECASE)
    ram_size_pattern = re.compile(fr'\b({"|".join(map(re.escape, ram_sizes))})\b', flags=re.IGNORECASE)
    processor_pattern = re.compile(fr'\b({"|".join(map(re.escape, processors))})\b', flags=re.IGNORECASE)

    for desc in description:
        graphics_card_match = graphics_card_pattern.search(desc)
        gpu.append(graphics_card_match.group(1) if graphics_card_match else None)

        storage_size_match = storage_size_pattern.search(desc)
        storage.append(storage_size_match.group(1) if storage_size_match else None)

        ram_size_match = ram_size_pattern.search(desc)
        ram.append(ram_size_match.group(1) if ram_size_match else None)

        processor_match = processor_pattern.search(desc)
        processor.append(processor_match.group(1) if processor_match else None)
    #putting together the dataframe
    df = pd.DataFrame({"manufacturer" : manufacturer, "condition" : condition, "price" : price, 
                       "screen size" : screen, "processor" : processor, "ram" : ram, "disk size" : storage, 
                       "graphics card" : gpu, "description" : description})
    #cleaning the data
    for i in range(len(df)):
        df['price'][i] = df['price'][i].split("₮")[0].replace(',','')
        
    df['price'] = df['price'].astype(float)
    
    for i in range(len(df)):
        if df['price'][i] < 10.00:
            df['price'][i] = df['price'][i] * 1_000_000
            
    df['price'] = df['price'].astype(int)
    
    for i in range(len(df)):
        df['manufacturer'][i] = df['manufacturer'][i].replace('Бусад','other')
else:
    df = pd.read_csv('finaldf.csv')

################################################################################################################

st.sidebar.title('Filter Options')

price_range = st.sidebar.slider('Select Price Range', step=1000, min_value=df['price'].min(), max_value=df['price'].max(), 
                                value=(df['price'].min(), df['price'].max()))

selection = st.sidebar.selectbox('Select a Manufacturer',("All", "HP", "Lenovo", "Acer", "Asus", "Dell", 
                                                           "Apple", "Gateway", "other", "MSI", "Samsung",
                                                           "Evoo", "Sony", "Microsoft Surface"))
used = st.sidebar.selectbox('Sort by Condition',("All","New","Used"))

if selection == "All":
    filtered_df = df
else:
    filtered_df = df[df['manufacturer'] == selection]

filtered_df1 = filtered_df[(filtered_df['price'] >= price_range[0]) & (filtered_df['price'] <= price_range[1])]

if used == "All":
    filtered_df2 = filtered_df1
else:
    filtered_df2 = filtered_df1[filtered_df1['condition'] == used]

show_description = st.sidebar.checkbox('Show Description', value=False)

if not show_description:
    filtered_df3 = filtered_df2.drop('description', axis=1)
else:
    filtered_df3 = filtered_df2
    
show_nans = st.sidebar.checkbox('Hide Nan Values', value=False)
if show_nans:
    filtered_df4 = filtered_df3.dropna()
else:
    filtered_df4 = filtered_df3
    
st.dataframe(filtered_df4, width=3000)


st.write(f'### Bar Chart of Avg Price per Manufacturer')
avg_price_by_manufacturer = df.groupby('manufacturer')['price'].mean()
st.bar_chart(avg_price_by_manufacturer)

st.write(f'### Line Chart for Prices by Manufacturer')
for manufacturer, data in df.groupby('manufacturer'):
    st.write(manufacturer)
    st.line_chart(data['price'].reset_index(drop=True))
