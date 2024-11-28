import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plotMap():
  df = pd.read_csv('./data/data.csv', index_col=0)

  center = dict(lat=-8.0513, lon=-34.9313)
  # fig = px.scatter_mapbox(df, lat="lat", lon="lng", hover_name="title", hover_data=["title", "price", "url",],
  fig = px.scatter_map(df, lat="lat", lon="lng", hover_name="title", hover_data=["title", "price", "url",],
  color_discrete_sequence=["red"], zoom=13, height=700, center=center, opacity=0.2,
  size=[15 for i in range(len(df))], )
  
  fig.update_layout({"scattermode":"group"})
  # print('file updated!')
  # fig.update_layout(mapbox_style="carto-positron")
  
  
  # fig.show()
  fig_json = fig.to_json()
  with open('plot.json', 'w') as fd:
    fd.write(fig_json)
  with open('./gmme-map/static/plot.json', 'w') as fd:
    fd.write(fig_json)
    print('plotly scatter map has been saved as "plot.json"')


# PLOTLY FIGURE METHODS CONVENTIONS

# fig.update_layout(title_text="update_layout() Syntax Example",
#                   title_font=dict(size=30))


# fig.update_layout(title=dict(text="update_layout() Syntax Example"),
#                              font=dict(size=30))

# USE EITHER THE FIRST OR LAST ONE BELOW:
# fig.update_layout(title_text="update_layout() Syntax Example",
#                   title_font_size=30)

# fig.update_layout({"title": {"text": "update_layout() Syntax Example",
#                              "font": {"size": 30}}})

# fig.update_layout(title=go.layout.Title(text="update_layout() Syntax Example",
#                                         font=go.layout.title.Font(size=30)))

# Testing
# plotMap()