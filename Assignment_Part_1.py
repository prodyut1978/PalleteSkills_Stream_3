import pandas as pd
import geopandas as gpd
import plotly.express as px


url = 'https://en.wikipedia.org/wiki/List_of_countries_by_wheat_production'

df=pd.read_html(url)[0]
df.rename(columns={"2020[1]": "2020", "2021[1]": "2021", "2022[1]": "2022"}, inplace=True)
wheat_data = df[['Country', '2020', '2021', '2022']]
wheat_data = wheat_data.dropna()
wheat_data['Average_Production'] = wheat_data[['2020', '2021', '2022']].mean(axis=1)
print(wheat_data.head())
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'), engine="pyogrio")
print(world.head())
merged = world.merge(wheat_data, left_on='name', right_on='Country', how='left')

fig = px.choropleth(merged,
                    locations="name", 
                    locationmode="country names", 
                    color="Average_Production",
                    hover_name="name", 
                    projection="natural earth",
                    title="Average Wheat Production by Country (2020-2022)",
                    color_continuous_scale=px.colors.sequential.Plasma)

fig.show()