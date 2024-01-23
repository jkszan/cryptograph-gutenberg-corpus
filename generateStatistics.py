from src.ngram import generateAllNgramCounts, aggregateCounts

def compileSpaced():
    generateAllNgramCounts(spacesRemoved=False)
    aggregateCounts(spacesRemoved=False)

def compileSpacesRemoved():
    generateAllNgramCounts(spacesRemoved=True)
    aggregateCounts(spacesRemoved=True)

compileSpaced()
compileSpacesRemoved()
