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

url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
print('Classes of each table:')
for table in soup.find_all('table'):
    print(table.get('class'))

table = soup.find('table', {'class': 'wikitable'})
df = pd.read_html(str(table))[0]
df.columns = ['Rank', 'Country', 'Population', 'Percentage', 'Date', 'Source', 'Notes']
df = df[['Country', 'Population']]
merged = world.merge(df, left_on='name', right_on='Country', how='left', indicator=True).query('_merge == "both"')
merged_Failed_Country = world.merge(df, left_on='name', right_on='Country', how='right', indicator=True).query('_merge != "both"')
merged_Failed_name = world.merge(df, left_on='name', right_on='Country', how='left', indicator=True).query('_merge != "both"')

fig = px.choropleth(
    merged,
    geojson=merged.geometry,
    locations=merged.index,
    color="Population",
    hover_name="name",
    hover_data=["Population"],
    projection="natural earth",
    title="World Population by Country",
    color_continuous_scale=px.colors.sequential.Plasma
)
fig.show()


