
import json

with open("data.json") as json_data :
    gameData = json.load(json_data)


def updateFile() -> None :
    """Mise a jour du fichier json
    """
    dataFile = open("data.json", "w")
    json.dump(gameData, dataFile, indent=2)
    dataFile.close()


def connect(login:str) -> dict:
    """Connexion a un compte, ou création de celui-ci s'il n'existe pas

    Args:
        login (str): nom du joueur (unique à chaque joueur)

    Returns:
        dict: objet joueur
    """

    # Si le joueur existe déjà, le connecter
    if login in gameData :
        user = gameData[login]
    # Sinon créer une joueur et le connecter
    else :
        gameData[login] = {"nbGames" : 0, "bestScore" : None, "lastScore" : None}
        user = gameData[login]
        updateFile()
    
    return user


def getLastScore(user:dict) -> str :
    """Récupération du dernier score

    Args:
        user (dict): Objet utilisateur

    Returns:
        str: Ancien score
    """
    # Si l'utilisateur n'as pas encore de score
    if user["lastScore"] == None :
        lastScore = "Aucun score"
    # Sinon renvoyer son ancien score
    else :
        lastScore = str(user["lastScore"])
    return lastScore


def getAccounts() -> list :
    """Récupération de tous les noms des joueurs existants

    Returns:
        list: liste des nom de joueurs
    """
    return list(gameData.keys())


def getAccountInfos(accountName:str) -> tuple :
    """Récupération des informations d'un compte

    Args:
        accountName (str): Nom du compte

    Returns:
        tuple: Infos du compte
    """
    if accountName not in gameData :
        raise ValueError("Joueur inexistant")
    return ( gameData[accountName]["nbGames"], gameData[accountName]["bestScore"], gameData[accountName]["lastScore"] )


def getBestScore(user:dict) -> str : 
    """Récupération du meilleur score

    Args:
        user (dict): _description_

    Returns:
        str: _description_
    """

    # S'il n'y a pas encore de score enregistré
    if user["lastScore"] == None :
        bestScore = "Aucun score"
    # Sinon récupérer le meilleur score
    else :
        bestScore = str(user["lastScore"])
    return bestScore


def updateScores(user:dict, newScore:int) :
    """Mettre a jout les scores du joueur

    Args:
        user (dict): objet utilisateur
        newScore (int): nouveau score
    """
    # Ajout du nouveau score comme dernier score enregistré
    user["lastScore"] = newScore
    # Si le score dépasse le meilleur score, alors le mettre comme meilleur score
    if user["bestScore"] == None or newScore > user["bestScore"] :
        user["bestScore"] = newScore
    # Augmentation du nombre de parties jouées de 1
    user["nbGames"] += 1
    updateFile()


def resetData() :
    """Remise à zéro des données
    """
    gameData.clear()
    updateFile()