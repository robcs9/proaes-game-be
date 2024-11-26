import plotly.express as px
import plotly.graph_objects as go
from jinja2 import Template

# fig = px.scatter(x=range(10), y=range(10))
# fig.write_html("plot.html")
# html = fig.to_html(full_html=False)

data_canada = px.data.gapminder().query("country == 'Canada'")
# fig = px.bar(data_canada, x='year', y='pop')

# import numpy as np
# np.random.seed(1)

# x = np.random.rand(100)
# y = np.random.rand(100)

# fig = go.FigureWidget([go.Scatter(x=x, y=y, mode='markers')])

# scatter = fig.data[0]
# colors = ['#a3a7e4'] * 100
# scatter.marker.color = colors
# scatter.marker.size = [10] * 100
# fig.layout.hovermode = 'closest'


# def handle_click():
#     fig.update_traces(marker_color='red')

# fig.on_click(handle_click)

from ipywidgets import Output, VBox

# Create a FigureWidget
fig = go.FigureWidget(data=[go.Bar(x=[1, 2, 3], y=[4, 5, 6])])

# Prepare Output to capture the clicks
out = Output()
@out.capture(clear_output=True)
def handle_click(trace, points, state):
    # Handle the click event
    print(f"Clicked on point index: {points.point_inds[0]}")

# Attach the on_click handler to the trace
fig.data[0].on_click(handle_click)

# Display the FigureWidget and Output
VBox([fig, out])


output_html_path=r"plot.html"
input_template_path = r"template.html"

plotly_jinja_data = {"fig":fig.to_html(full_html=False)}
#consider also defining the include_plotlyjs parameter to point to an external Plotly.js as described above

with open(output_html_path, "w", encoding="utf-8") as output_file:
    with open(input_template_path) as template_file:
        j2_template = Template(template_file.read())
        output_file.write(j2_template.render(plotly_jinja_data))