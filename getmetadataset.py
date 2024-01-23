import pandas as pd
from collections import defaultdict

def compile_stats():
    metadata = pd.read_csv("metadata/metadata.csv").set_index("id")
    print(len(metadata))
    filtered_meta = metadata[metadata["language"].str.contains("en")]
    print(filtered_meta['language'].head(20))
    print(len(filtered_meta))
    print(filtered_meta.columns)

    yearOfDeathStats = defaultdict(lambda: 0)
    yearOfBirthStats = defaultdict(lambda: 0)
    birthNum = 0
    deathNum = 0

    for index, (title, _, yearBirth, yearDeath, language, _, _, btype) in filtered_meta.iterrows():
        try:
            yearInt = int(yearBirth)
            yearOfBirthStats[yearInt] += 1
            birthNum += 1

        except:
            yearOfBirthStats["Undefined"] += 1

        try:
            yearInt = int(yearDeath)
            yearOfDeathStats[yearInt] += 1
            deathNum += 1
        except:
            yearOfDeathStats["Undefined"] += 1
    
    print(yearOfBirthStats)
    print("----")
    print(yearOfDeathStats)
    print(birthNum, deathNum)

    diedAfter2000 = 0
    for year, num in yearOfDeathStats.items():
        if type(year) == int and year >= 1970:
            diedAfter2000 += num

    print(diedAfter2000)

    selectedBooks = []
    for index, (title, _, yearBirth, yearDeath, language, _, _, btype) in filtered_meta.iterrows():
        try:
            yearInt = int(yearDeath)
            if yearInt >= 1970:
                selectedBooks.append(index)
        except:
            pass
    print(selectedBooks)


compile_stats()