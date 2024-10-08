import requests
import pandas as pd
import geopandas as gpd
import plotly.express as px
from bs4 import BeautifulSoup

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'), engine="pyogrio")
world.loc[world['name'] == 'United States of America', 'name'] = 'United States'
world.loc[world['name'] == 'Greenland', 'name'] = 'Greenland (Denmark)'
world.loc[world['name'] == 'Dem. Rep. Congo', 'name'] = 'Democratic Republic of the Congo'
world.loc[world['name'] == 'S. Sudan', 'name'] = 'Sudan'


url_Wheat = 'https://en.wikipedia.org/wiki/List_of_countries_by_wheat_production'
response = requests.get(url_Wheat)
soup = BeautifulSoup(response.text, 'html.parser')
print('Classes of each table:')
for table in soup.find_all('table'):
    print(table.get('class'))

table = soup.find('table', {'class': 'wikitable'})
wheat_df = pd.read_html(str(table))[0]
wheat_df= (wheat_df.loc[:,['Country','2022[1]']])
wheat_df.rename(columns={"Country": "Country","2022[1]": "Production_2022"}, inplace=True)

print(len(wheat_df))

url_Pop = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'
response = requests.get(url_Pop)
soup = BeautifulSoup(response.text, 'html.parser')
print('Classes of each table:')
for table in soup.find_all('table'):
    print(table.get('class'))

table = soup.find('table', {'class': 'wikitable'})
Pop_df = pd.read_html(str(table))[0]
Pop_df.columns = ['Rank', 'Country', 'Population', 'Percentage', 'Date', 'Source', 'Notes']
Pop_df = Pop_df[['Country', 'Population']]
Pop_df.loc[Pop_df['Country'] == 'Czech Republic', 'Country'] = 'Czechia'

print(len(Pop_df))


merged_df_Pop_Wheat = pd.merge(wheat_df, Pop_df, on='Country', how='inner', indicator=True)

merged_df_Pop_Wheat['Wheat_per_million'] = (merged_df_Pop_Wheat['Production_2022'] / merged_df_Pop_Wheat['Population']) * 1e6

print(len(merged_df_Pop_Wheat))

merged = world.merge(merged_df_Pop_Wheat, left_on='name', right_on='Country', how='right')

print(len(merged))



fig = px.choropleth(
      merged,
      geojson=merged.geometry,
      locations=merged.index,
      color='Wheat_per_million',
      hover_name='Country',
      hover_data=['Production_2022', 'Population', 'Wheat_per_million'],
      projection='natural earth',
      title='2022 Wheat Production per 1 Million People by Country',
      color_continuous_scale=px.colors.sequential.Plasma
)

fig.show()