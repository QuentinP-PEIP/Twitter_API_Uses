# -*- coding: utf-8
"""
@author: romain
"""
# importation de toutes les librairies nécessaires
import sys
import json
import tweepy

# entré des clés d'accès pour accéder à l'api de Twitter
ACCESS_TOKEN = '3630486686-t9KRvopuFRBx1gcSMPNm7Az42IuOYzsnniYC8Ov'
ACCESS_SECRET = 'Ao7yOVkEdV9YwjifVKc0fYJ9HBaCtt1irCYz93yqtYfFA'
CONSUMER_KEY = 'cQS31eTih0ze6zUcS53xGYKM5'
CONSUMER_SECRET = '5M4klAwE0TsUfXYQOssD2NnfUzuuWOfkVUAztBYeWDQDIqo2oY'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)


class StreamListener(tweepy.StreamListener):
    num_tweets = 0

    def on_status(self, status):

        #Afficher le tweet et ces infos dans la consoles ainsi que son nuléro de collecte
        print(str(self.num_tweets) + " : " + str(status._json))
        # ajouter au a la liste de 'foo' les infos du tweet sous format json
        tweet['foo'].append(status._json)
        self.num_tweets = self.num_tweets + 1
        # On vérifie si on a recupérer assez de tweet par rapport à la valeur afficher
        if self.num_tweets == 2000:
            # Ecriture du dictionnaire tweet dans le fichier json
            with open('BaseTweet2.json', 'w') as tweetBank:
                json.dump(tweet, tweetBank)
            sys.exit(0)
        return True

    def on_error(self, status_code):
        if status_code == 420:
            return False

# Création du dictionnaire avec comme clé foo, et comme valeur une liste
tweet = {'foo': []}

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
# Récupérer que les tweets dans ces coordonées géographique (autour de la france métropolitaine
# La langue doit être francaise
stream.filter(locations=[-4.254036, 42.393329, 8.339372, 51.756766], languages=['fr'])
