import pandas
import pandas as pd

from name_list import NameList


_song_name_df = pd.read_csv("names/allNames.csv", header=0)
_song_name_df.sort_values(by="highestRank", inplace=True)
song_names = NameList(list(_song_name_df["name"].unique()))


_baby_name_df = pd.read_csv("names/babynames-clean.csv", names=["name", "gender"])
_baby_name_lists = [
    list(_baby_name_df.loc[_baby_name_df["gender"].eq(gender)]["name"])
    for gender in ["boy", "girl"]
]
_final_babies = []
for name_list in _baby_name_lists:
    _final_babies += name_list[100:] + name_list[:100]
baby_names = NameList(_final_babies, 3)

print("x")
