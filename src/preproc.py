import os
from pprint import pprint
import itertools
from pandas import read_csv, DataFrame, Series

process_all_files = False
reprocess = False
file_dir = "../data/"
match_file = file_dir + "matchinfo.csv"
champ_file = file_dir + "champs.csv"
dataframes = {}

# Creates Primary data set: datum = (red, blue, result)
# Result is 1 for red victory, 0 for blue victory 
def extractChamps(champ_frame):
    champs = extract(champ_frame, "Champ")
    red = extract(champs, "red")
    blue = extract(champs, "blue")
    results = extract(champ_frame, "rResult")
    data = DataFrame()

    for i in range(len(red)):
        redTeam = sorted(red.iloc[i].tolist())
        if i % 500 == 0:
            print(f"\niteration {i}:\nRed Team: {redTeam}")
        blueTeam = sorted(blue.iloc[i].tolist())
        if i % 500 == 0:
            print(f"Blue Team: {blueTeam}")
        datum = {"red" : redTeam, "blue" : blueTeam, "results" : results.iloc[i].tolist()[0]}
        data = data.append(datum, ignore_index=True)
    data.to_csv(champ_file, header=False, index=False)
    return data

# Given a DataFrame, returns a Dataframe of columns containing 
# filter_key in the header.
def extract(frame, filter_key):
    headers = list(frame.columns.values)
    keys = [key for key in headers if filter_key in key]
    return frame.filter(keys, axis=1)

def process_all():
    for filename in os.listdir(file_dir):
        name = filename.split(".")[0] # cut out '.csv' extension
        path = f"{file_dir}/{filename}"
        print(f"Preprocessing {name}...")
        with open(path, encoding="utf-8") as fileObj: ### errors="backslashreplace"
            dataframes[name] = read_csv(fileObj)
            if name == match_file:
                dataframes["champs"] = extractChamps(dataframes[name])

def getChamps():
    if os.path.exists(champ_file) and not reprocess:
        dataframes["champs"] = read_csv(champ_file, header=None)
        return
    with open(champ_file, "w", encoding="utf") as fileObj:
        dataframes["champs"] = extractChamps(read_csv(match_file))

if process_all_files:
    process_all()
else:
    getChamps()
    
print("Dataframe Shapes:")
for key in dataframes.keys():
    print(f"\t{key}: {dataframes[key].shape}")
