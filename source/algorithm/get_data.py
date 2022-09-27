import numpy as np
import pandas as pd
from PIL import Image


def get_data_from_coords_and_file(x_list, y_list, filename):
    im = np.array(Image.open(filename))
    return im[x_list, y_list]


def get_data_df(coords, features_files):
    data = {}
    data["x"] = coords[0]
    data["y"] = coords[1]
    for feature, filename in features_files:
        data[feature] = get_data_from_coords_and_file(coords[0], coords[1], filename)
    return pd.DataFrame.from_dict(data)


def get_coords_from_file(filename):
    lines = []
    with open(filename, "r") as f:
        lines = f.readlines()
        lines = lines[1:]
    coords = [[], []]
    for line in lines:
        _, x, y = line.split()
        coords[0].append((int(x) - 310050) // 100)
        coords[1].append((int(y) - 4800050) // 100)
    return coords

def correct_indexes():
    mask = np.ones((4096, 4096))
    vineyards = np.array(Image.open("data/KRA_VINEYARDS_100m.tif"))
    mask[vineyards == True] = 0
    landcover = np.array(Image.open("data/KRA_LANDCOVER_100m.tif"))
    mask[(landcover == 1) | (landcover == 7) | (landcover == 8) | (landcover == 9)] = 0
    # water = np.array(Image.open("data/KRA_WATER_SEASONALYTY_100m.tif"))
    # mask[(water > 0)] = 0
    # admin = np.array(Image.open("data/KRA_ADMIN_100m.tif"))
    return np.argwhere(mask == 1)