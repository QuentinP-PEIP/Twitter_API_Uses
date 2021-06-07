# -*- coding: utf-8 -*-
"""
@author: romain
"""
# Importation des librairies necessaires.
import folium
import webbrowser
import json
import re
from stop_words import get_stop_words

# Ouverture du document contenant les tweets collecté à l'aide du fichier getTweet.py
with open('BaseTweet.json') as tweetBank:
    data = json.load(tweetBank)
    tweets = data.get("foo")

# Création de la map, centré sur la France
m = folium.Map(location=[47, 2], zoom_start=6, tiles='OpenStreetMap')

donnee = []

# Création de la liste des mots interdits, avec ajout de quelques mots apercus lors des tests
list_interdit = get_stop_words("fr")
list_interdit += ["", " ", "cest", "bien", "veut", "rien", "plus", "toujours", "hui", "jai", "hein", "co", "voilà",
                  "voila", "vraiment", "vient", "merci", "c'est", "j'ai", "j'avais", "t'es", "n'est", "non", "ah", "oh"]


# Fonction retournant vrai si un des dico dans la liste donnée à pour clé la ville mis en argument
def exist_dico(ville):
    for dico in donnee:
        if dico["Ville"] == ville:
            return True
    return False


# Fonction retournant vrai si le mot en argument est une des clés du dictionnaire en argument
def exist_mot(dico, mot):
    if dico.get(mot, False):
        return True
    else:
        return False


# Fonction remplacant toutes les ponctuation cité dans la liste  ainsi que tous les chiffres par "" (vide)
def del_ponctuation(t):
    list_ponctuation = ["?", ",", ".", ";", "/", ":", "!", '"', "(", ")", "\n", "`", "’", "…", "_", "#", "-"]

    for ponctuation in list_ponctuation:
        t = t.replace(ponctuation, "")
    for i in range(0, 10):
        t = t.replace(str(i), "")
    return t


# Fonction retournant un dictionnaire ayant pour clés tous les mots de la liste et pour valeur, leurs nombres d'appartition
def dico_mots(liste):
    mots = {}
    res = []
    for phrase in liste:
        for m in phrase.split():
            m = m.lower()
            m = del_ponctuation(m)
            if m not in list_interdit:
                # Verifictation que ce n'est pas un lien ou bien un tag de personne, et que ce ne soit pas un simple caractère
                if not re.search(r"^https.*", m) and not re.search(r"^@.*", m) and len(m) != 1:
                    res.append(m)
        for mot in res:
            if exist_mot(mots, mot) == False:
                mots[mot] = 1
            else:
                mots[mot] += 1
    return mots


# Retourne le premier mots du dictionnaire apparaissant le plus de fois
def max_use(dico):
    i = 0
    top = ""
    for key in dico.keys():
        if dico[key] > i:
            i = dico[key]
            top = key
    return top


# Crée et renvoie une liste ayant les 3 mots les plus utilisés
def top_mots(dico):
    top = []
    i = 0
    while i < 3:
        mot = max_use(dico)
        if mot != "":
            top.append(mot)
            del dico[mot]
        i += 1
    return top


# Pour tous les tweets récupéré
for tweet in tweets:
    ville = tweet["place"]["name"]  # Nom de la ville
    if not exist_dico(ville):
        dico = {"Ville": ville, "nombre": 1}  # Création du dictionnaire de la ville avec son nombre de tweet
        # Création des coordonnés ( a peu près le centre en prenant le centre de la diagonale)
        coox = tweet["place"]["bounding_box"]["coordinates"][0][0][0] + (
                tweet["place"]["bounding_box"]["coordinates"][0][2][0] -
                tweet["place"]["bounding_box"]["coordinates"][0][0][0]) / 2
        cooy = tweet["place"]["bounding_box"]["coordinates"][0][0][1] + (
                tweet["place"]["bounding_box"]["coordinates"][0][1][1] -
                tweet["place"]["bounding_box"]["coordinates"][0][0][1]) / 2
        dico["coord"] = [cooy, coox]
        dico["texte"] = [tweet["text"]]
        donnee.append(dico)
    else:
        # Si le dictionnaire existe deja, ajout de 1 au nombre de tweet et ajout du texte du nouveau tweet
        for dico in donnee:
            if dico["Ville"] == ville:
                dico["nombre"] += 1
                dico["texte"].append(tweet["text"])

# Affichage sur la carte
for ville in donnee:
    city = ville["Ville"]
    nb_tweet = len(ville["texte"])
    if nb_tweet < 5:
        # Si le nombre de tweet est inférieur à 5 pour une ville, alors elle n'apparait pas sur la carte
        continue
    top_mot = top_mots(dico_mots(ville["texte"]))
    nb = len(top_mot)
    coord = ville["coord"]
    html = f"""
            <h1> {city}</h1>
            <p>Nombre de tweets: {nb_tweet}</p>
            <p>Mots les plus fréquents:</p>
            <ul>
                <li>{top_mot[0]}</li>
                <li>{top_mot[1]}</li>
                <li>{top_mot[2]}</li>
            </ul>
            """
    iframe = folium.IFrame(html=html, width=200, height=200)
    popup = folium.Popup(iframe, max_width=2650)
    folium.Marker(coord,
        popup=popup,
        icon=folium.Icon(icon='info-sign', color='blue')
    ).add_to(m)


m.save('index.html')
webbrowser.open('index.html')
