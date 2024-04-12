from csv_wrangler import baby_names, song_names

for i in range(100):
    print(f"{baby_names.get()[0]}, {song_names.get()[0]}")
