import numpy as np
import json

with open("data.json") as json_data :
    gameData = json.load(json_data)


def updateFile() -> None :
    """Mise a jour du fichier json
    """
    dataFile = open("data.json", "w")
    json.dump(gameData, dataFile, indent=2)
    dataFile.close()


def setScores(newScore:int) :
    """Mise a jout des scores

    Args:
        newScore (int): Nouveau score
    """
    gameData["lastScore"] = newScore
    if gameData["bestScore"] == None or newScore > gameData["bestScore"] :
        gameData["bestScore"] = newScore
    
    updateFile()

def getBestScore():
    """Getter du meilleur score

    Returns:
        str : Meilleur score enregistré
    """
    if gameData["bestScore"] == None :
        bestScore = "Aucun"
    else :
        bestScore = str(gameData["bestScore"])
    
    return bestScore


def getLastScore():
    """Getter du dernier score

    Returns:
        str: Le dernier score
    """
    if gameData["lastScore"] == None :
        lastScore = "Aucun"
    else :
        lastScore = str(gameData["lastScore"])
    
    return lastScore