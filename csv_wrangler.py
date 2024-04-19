from time import time

import pandas as pd

from name_list import NameList

NameList.seed = time()

name_lists = []


_song_name_df = pd.read_csv("names/allNames.csv", header=0)
_song_name_df.sort_values(by="highestRank", inplace=True)
song_names = NameList(list(_song_name_df["name"].unique()), priority=-5)
name_lists.append(song_names)


_baby_name_df = pd.read_csv("names/babynames-clean.csv", names=["name", "gender"])
_baby_name_lists = [
    list(_baby_name_df.loc[_baby_name_df["gender"].eq(gender)]["name"])
    for gender in ["boy", "girl"]
]
_final_babies = []
for name_list in _baby_name_lists:
    _final_babies += name_list[100:] + name_list[:100]
baby_names = NameList(_final_babies, 3, 2)
name_lists.append(baby_names)


_forenames_by_country_df = pd.read_csv(
    "names/common-forenames-by-country.csv", header=0
)
forenames_country = NameList(
    list(_forenames_by_country_df["Romanized Name"]), priority=20, default_count=3
)
name_lists.append(forenames_country)


_surnames_by_country_df = pd.read_csv("names/common-surnames-by-country.csv", header=0)
forenames_country = NameList(
    list(_forenames_by_country_df["Romanized Name"]), priority=18, default_count=2
)
name_lists.append(forenames_country)


name_lists.sort(key=lambda x: x.priority, reverse=True)


def wrangle_names():
    print("; ".join(str(nl) for nl in name_lists))


for i in range(10):
    wrangle_names()
