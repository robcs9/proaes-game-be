import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# retrieving overlapping locations to be handled later as markers/traces
def scatterOverlaps(df:pd.DataFrame=None):
  # df = pd.read_csv('./data/data.csv', index_col=0)
  grouping = df[df.duplicated(['lat', 'lng'], keep=False)].groupby(['lat', 'lng'], as_index=False)
  # filtered_list = grouped_df.agg(list)
  # print(grouped_df.groups)
  # print(grouping.get_group((-8.055802, -34.921399)))
  no_overlap_df = handleOverlapsCoords(df, grouping)
  return no_overlap_df


from pandas.core.groupby.generic import DataFrameGroupBy
def handleOverlapsCoords(df:pd.DataFrame=None, grp: DataFrameGroupBy=None):
  # for row in group.groups
  # print(dir(group.groups))
  # print(grp.groups.keys())
  for name, group in grp:
    # print(group.index)
    lat = name[0]
    lon = name[1]
    curr_lat = lat
    curr_lon = lon
    # print(f'original ({lat}, {lon})')
    # for idx in group.index:
    #   curr_lat = curr_lat * 0.999
    #   curr_lon = (curr_lon + 0.999) % lon
    #   df.loc[idx, "lat"] = curr_lat
    #   df.loc[idx, "lng"] = curr_lon
    #   # print(f'current ({curr_lat}, {curr_lon})')
    for idx in group.index:
      distance = 0.001
      # curr_lat += 0.999
      curr_lon += distance
      df.loc[idx, "lat"] = curr_lat
      df.loc[idx, "lng"] = curr_lon
      # print(f'current ({curr_lat}, {curr_lon})')
  return df

def plotMap():
  df = pd.read_csv('./data/data.csv', index_col=0)
  df = scatterOverlaps(df)
  center = dict(lat=-8.0513, lon=-34.9313)
  fig = px.scatter_map(df, lat="lat", lon="lng", hover_name="title", hover_data=["title", "price", "url",],
  color_discrete_sequence=["red"], zoom=13, height=700, center=center, opacity=0.2,
  size=[15 for i in range(len(df))], )
  
  # fig.layout.title.text = 'some text1'
  fig.update_layout(go.Layout(title='some text3',))
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