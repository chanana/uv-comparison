import base64

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State

from functions import (
    calculate_cosine_all_v_all,
    calculate_L2_norm_all_v_all,
    make_and_cleanup_dataframe,
    read_opus_data,
)
from html_functions import make_heatmap_from_distance_matrix

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SKETCHY],
    prevent_initial_callbacks=True,
)

upload_files_button = dcc.Upload(
    id="upload-data-multiple",
    children=dbc.Button("Upload IR files", color="primary"),
    multiple=True,
)
euc_cosine_radio = html.Div(
    [
        dbc.Label("Choose one"),
        dbc.RadioItems(
            id="euclidean-or-cosine",
            options=[{"label": i, "value": i} for i in ["euclidean", "cosine"]],
            value="euclidean",
            inline=True,
        ),
    ]
)
download_button = html.Div(
    [
        dbc.Button("Download CSV", color="success", id="download-btn"),
        dcc.Download(id="download-distance-matrix"),
    ]
)
buttons_and_selectors = dbc.Row(
    [
        dbc.Col(upload_files_button, width=3),
        dbc.Col(euc_cosine_radio, width=3),
        dbc.Col(download_button, width=3),
    ],
    align="center",
    justify="center",
)

figure = dbc.Row(dbc.Col(children=[dcc.Graph(id="L2-heatmap", figure={})]))
storage = dcc.Store("storage-similarity-matrix")
app.layout = dbc.Container([buttons_and_selectors, figure, storage])


@app.callback(
    Output("download-distance-matrix", "data"),
    Input("download-btn", "n_clicks"),
    State("storage-similarity-matrix", "data"),
    State("euclidean-or-cosine", "value"),
    prevent_initial_call=True,
)
def download_data(n_clicks, stored_df, euc_or_cos):
    df = pd.read_json(stored_df, orient="split")
    return dcc.send_data_frame(df.to_csv, str(euc_or_cos) + "_mat.csv")


@app.callback(
    Output("L2-heatmap", "figure"),
    Output("storage-similarity-matrix", "data"),
    Input("upload-data-multiple", "contents"),
    Input("euclidean-or-cosine", "value"),
    State("upload-data-multiple", "filename"),
)
def convert_uploaded_files(list_of_contents, distance_metric, list_of_filenames):
    if list_of_contents is not None:
        df = pd.DataFrame(data=None)
        x_values = None
        for content, filename in zip(list_of_contents, list_of_filenames):
            content_type, content_string = content.split(",")
            decoded = base64.b64decode(content_string)
            x, y = read_opus_data(decoded)

            df[filename] = y

            # we just need one set of x_values that will be common across all files
            if x_values is None:
                x_values = x

        clean_df = make_and_cleanup_dataframe(dataframe=df, columns=x_values)
        if distance_metric == "euclidean":
            distance_matrix = calculate_L2_norm_all_v_all(clean_df)
        elif distance_metric == "cosine":
            distance_matrix = calculate_cosine_all_v_all(clean_df)
        storage_df = pd.DataFrame(
            data=distance_matrix, index=clean_df.index, columns=clean_df.index
        )
        fig = make_heatmap_from_distance_matrix(
            distance_matrix, clean_df.index, clean_df.index
        )
        return fig, storage_df.to_json(orient="split")


if __name__ == "__main__":
    app.run_server(host="0.0.0.0")
