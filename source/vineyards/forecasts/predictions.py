import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from pyproj import Proj, transform

x_base = 310050
y_base = 4800050 + 4096 * 100


def convert_coordinates(x, base):
    return (x - base) / 100


def from_picture_to_map(point):
    inProj = Proj("+init=EPSG:32637", preserve_units=True)
    outProj = Proj("+init=EPSG:4326")  # WGS84 in degrees and not  in meters)
    # swap x,y as mkennedy says
    x1, y1 = point[0] * 100 + x_base, -point[1] * 100 + y_base
    coords = transform(inProj, outProj, x1, y1)
    return coords[1], coords[0]


def get_top_vineyard(desired, lands, k=3):
    desired = desired.drop(["x", "y"], axis=0)
    lands = lands.drop(["x", "y"], axis=1)
    desired = np.array([np.array(desired, dtype=float)])
    lands = np.array(lands, dtype=float)
    distances = cdist(desired, lands)[0]
    closest_lands = lands[np.argpartition(distances, k)[:k]]
    distances = cdist(desired, closest_lands)[0]
    return np.argsort(distances)


def find_closest(wineyards_x, wineyards_y, k):
    wineyards = pd.read_csv("../data.csv")
    lands = pd.read_csv("../lands.csv")
    desired_wineyards = pd.DataFrame(columns=lands.columns)
    for i in range(len(wineyards_x)):
        s = wineyards.where(wineyards.x == wineyards_x[i]).where(wineyards.y == wineyards_y[i]).iloc[0]
        desired_wineyards = desired_wineyards.append(s)

    des = desired_wineyards.mean()
    # print(des)
    needed_indices = get_top_vineyard(des, lands, k)
    areas = pd.read_csv("../land_area.csv")
    ans = {
        "x_center": [],
        "y_center": [],
        "x_left": [],
        "x_right": [],
        "y_top": [],
        "y_bottom": [],
    }
    for i in range(k):
        area = areas[(areas.x == lands.iloc[needed_indices[i]].x) & (areas.y == lands.iloc[needed_indices[i]].y)]
        ans["x_center"].append(int(area.x))
        ans["y_center"].append(int(area.y))
        ans["x_left"].append(int(area.x_left))
        ans["x_right"].append(int(area.x_right))
        ans["y_top"].append(int(area.y_top))
        ans["y_bottom"].append(int(area.y_bottom))
    return ans
