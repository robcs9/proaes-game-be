import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('./data/data.csv', index_col=0)

center = dict(lat=-8.0513, lon=-34.9313)
# fig = px.scatter_mapbox(df, lat="lat", lon="lng", hover_name="title", hover_data=["title", "price", "url",],
fig = px.scatter_map(df, lat="lat", lon="lng", hover_name="title", hover_data=["title", "price", "url",],
color_discrete_sequence=["red"], zoom=13, height=700, center=center, opacity=0.4, size=[15 for i in range(len(df))], )
# fig.update_layout(mapbox_style="carto-positron")

fig_json = fig.to_json('plot.json')
with open('plot.json', 'w') as fd:
  fd.write(fig_json)
