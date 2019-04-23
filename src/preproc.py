import os
from pandas import read_csv

file_dir = "../data/"

champ_file = "matchinfo"
dataframes = {}

def extractChamps(champ_frame):
    champs = extract(champ_frame, "Champ")
    red = extract(champs, "red")
    blue = extract(champs, "blue")
    return red, blue

    
def extract(frame, filter_key):
    headers = list(frame.columns.values)
    keys = [key for key in headers if filter_key in key]
    return frame.filter(keys, axis=1)
    
for filename in os.listdir(file_dir):
    name = filename.split(".")[0] # cut out '.csv' extension
    path = f"{file_dir}/{filename}"
    print(f"Preprocessing {name}...")
    with open(path, encoding="utf-8") as fileObj: ### errors="backslashreplace"
        dataframes[name] = read_csv(fileObj)
        if name == champ_file:
            red, blue = extractChamps(dataframes[name])
            dataframes["red"] = red
            dataframes["blue"] = blue
            print(f"\n\n{dataframes['red']}\n\n")
            print(f"\n\n{dataframes['blue']}\n\n")

print("Dataframe Shapes:")

for key in dataframes.keys():
    print(f"\t{key}: {dataframes[key].shape}")
