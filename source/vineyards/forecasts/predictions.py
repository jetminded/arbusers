import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist


def get_top_vineyard(desired, lands, k=3):
    desired = np.array([np.array(desired, dtype=float)])
    lands = np.array(lands, dtype=float)
    distances = cdist(desired, lands)[0]
    closest_lands = lands[np.argpartition(distances, k)[:k]]
    distances = cdist(desired, closest_lands)[0]
    return np.argsort(distances)


def find_closest(wineyards_x, wineyards_y, k):
    wineyards = pd.read_csv("data.csv")
    lands = pd.read_csv("lands.csv")
    desired_wineyards = pd.DataFrame(columns=lands.columns)
    for i in range(len(wineyards_x)):
        s = wineyards.where(wineyards.x == wineyards_x[i]).where(wineyards.y == wineyards_y[i]).iloc[0]
        desired_wineyards = desired_wineyards.append(s)
    # print(desired_wineyards)
    des = desired_wineyards.mean()
    # print(des)
    needed_indices = get_top_vineyard(des, lands, k)
    ans_x = []
    ans_y = []
    for i in range(k):
        ans_x.append(lands.iloc[needed_indices[i]].x)
        ans_y.append(lands.iloc[needed_indices[i]].y)
    return ans_x, ans_y