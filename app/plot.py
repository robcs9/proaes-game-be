# import plotly.express as px
# import plotly.graph_objects as go
import pandas as pd
import numpy as np

# retrieving overlapping locations to be handled later as markers/traces
def scatterOverlaps(df:pd.DataFrame=None):
  if df is None:
    print(f'No overlapping points to scatter were found. DataFrame provided is None.')
    return
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
      if type(curr_lon) is not np.float64 and type(curr_lon) is not float:
        print(
          f"""Invalid longitude value during overlapping processing.
          longitude type: {type(curr_lon)}
          longitude value: {curr_lon}
          """
        )
        continue
      distance = 0.001
      # curr_lat += 0.999
      curr_lon += distance
      df.loc[idx, "lat"] = curr_lat
      df.loc[idx, "lng"] = curr_lon
      # print(f'current ({curr_lat}, {curr_lon})')
  return df