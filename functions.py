# functions.py contains functions that don't return html
import pandas as pd
import numpy as np


# def read_uv_json(opus_bytes):
#     meta_data = parse_meta(opus_bytes)
#     opus_data = parse_data(opus_bytes, meta_data)
#     x = [round(i) for i in opus_data.get_range("AB")[:-1]]
#     y = [round(i, 4) for i in opus_data["AB"][0 : len(x)]]

#     return x, y


def make_and_cleanup_dataframe(dataframe, columns):
    dataframe = dataframe.transpose()
    dataframe.columns = columns
    dataframe.sort_index(inplace=True)
    return dataframe


def calculate_L2_norm_all_v_all(dataframe):
    # assuming number of samples is number of rows
    diagonal_array = np.tri(dataframe.shape[0])

    for i in range(diagonal_array.shape[0]):
        a = dataframe.iloc[i, :].to_numpy()
        for j in range(diagonal_array.shape[1]):
            if diagonal_array[i][j] == 1 and i != j:
                b = dataframe.iloc[j, :].to_numpy()
                diagonal_array[i][j] = np.linalg.norm(a - b)
    return diagonal_array


def calculate_cosine_all_v_all(dataframe):
    # both functions def could have been combined...
    diagonal_array = np.tri(dataframe.shape[0])

    for i in range(diagonal_array.shape[0]):
        a = dataframe.iloc[i, :].to_numpy()
        for j in range(diagonal_array.shape[1]):
            if diagonal_array[i][j] == 1 and i != j:
                b = dataframe.iloc[j, :].to_numpy()
                diagonal_array[i][j] = (np.dot(a, b)) / (
                    np.linalg.norm(a) * np.linalg.norm(b)
                )
    return diagonal_array
