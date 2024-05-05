from time import time
import re

import pandas as pd

from name_list import NameList

NameList.seed = time()

name_lists = []


HAS_NUMBER = re.compile(r"\d")


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

CATEGORIES = ["black", "api", "aian", "hispanic"]
_census_df = pd.read_csv("names/Common_Surnames_Census_2000.csv")
_census_df.replace("(S)", "0.0", inplace=True)

census_name_lists = []
for category in CATEGORIES:
    _census_df[f"n{category}"] = _census_df["count"] * (
        _census_df[f"pct{category}"].astype(float)
    )
    census_name_lists.append(
        _census_df.sort_values(f"n{category}", ascending=False).iloc[:1000]["name"]
    )
# interleave names
census_name_list = [name for rank in zip(*census_name_lists) for name in rank]
census_names = NameList(census_name_list, priority=1, default_count=3, repetition=5)
name_lists.append(census_names)


_global_name_df = pd.read_csv("names/globalnames2.csv", header=0)
global_names = NameList(
    list(_global_name_df.iloc[-30000:-20000]["name"]), default_count=2
)
name_lists.append(global_names)


with open("names/street-names-1.csv") as f:
    _street_names_raw = f.readlines()
_street_names = [
    ((name.split(",")[0]).rsplit(" ", maxsplit=1)[0])
    for name in _street_names_raw
    if not HAS_NUMBER.match(name)
]
street_names = NameList(_street_names, default_count=2, priority=-10)
name_lists.append(street_names)


_unisex_name_df = pd.read_csv("names/unisex_names_table.csv", header=0)
unisex_names = NameList(list(_unisex_name_df["name"]), priority=-1, default_count=1)
name_lists.append(unisex_names)


_good_word_df = pd.read_csv("names/wordFrequency_nvj.csv", header=0)
_good_word_df = _good_word_df.loc[_good_word_df["rank"] > 100]
good_words = NameList(list(_good_word_df["lemma"]), priority=-80, default_count=3)
name_lists.append(good_words)


_all_word_df = pd.read_csv("names/en_50k.txt", names=["name", "rank"], sep=" ")
_all_word_df = _all_word_df.iloc[500:]
_all_word_df = _all_word_df.loc[_all_word_df["name"].apply(lambda x: len(str(x)) > 2)]
all_words = NameList(list(_all_word_df["name"]), priority=-100, default_count=4)
name_lists.append(all_words)


name_lists.sort(key=lambda x: x.priority, reverse=True)


def wrangle_names() -> str:
    return ";  ".join(str(nl) for nl in name_lists)


# for i in range(10):
#     print(wrangle_names())

with open("gen_names.txt", "wt", encoding="utf-8") as f:
    for i in range(1000):
        f.write(wrangle_names() + "\n\n")
