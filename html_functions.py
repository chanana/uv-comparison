from dash import dash_table
import plotly.graph_objects as go


def make_dash_table_from_dataframe(dataframe):
    return dash_table.DataTable(
        id="table",
        columns=[{"name": str(i), "id": str(i)} for i in dataframe.columns],
        data=dataframe.to_dict("records"),
        style_table={"overflowX": "scroll"},
    )


def make_heatmap_from_distance_matrix(distance_matrix, x_labels, y_labels=None):
    if y_labels is None:
        y_labels = x_labels
    fig = go.Figure(
        go.Heatmap(z=distance_matrix, x=x_labels, y=y_labels, colorscale="Viridis")
    )
    return fig
