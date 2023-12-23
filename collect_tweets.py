import tweepy
import datetime
import csv
import pandas as pd
import glob

# Initialisation & authentification
consumer_key='ygQx7iHz7QnIWNPDRJRUS1oKb'
consumer_secret='JYueM6S5WjTqe447qA00SPqlq6o3KS9USn2JFI0MZroBT8Iwub'
access_token='1599037496591015938-gFBzivu8mPvAsOZpgV1fX9bwr829i1'
access_token_secret='39RgeTMNW7CHPjeCzp6t7qHlD7wMFkOsJwzse6IwcmWXM'

# Connexion
auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret) 
auth.secure = True
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
# Collecte des données
# Requetes à identifier
query = "souveraineténumérique OR souverainetenumerique OR souverainete_numerique OR #souverainetenumerique OR souverainete-numerique"

# Création du fichier cvs pour sauvegarder les données collectées
dataset_T = datetime.datetime.now().strftime('data/dataset_T_%m-%d-%Y.csv')
with open(dataset_T, 'w', newline='', encoding="utf-8") as csvfile:
    headers = ['user_id', 'user_name', 't_user','retweet_count', 
                'favorite_count', 'created_at','retweeted','hashtags', 'user_mentions','text']
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(headers)

# Scrapping
    for page in tweepy.Cursor(api.search_tweets, q=query, count=2000, tweet_mode= 'extended').pages():
        rows = []
        for tweet in page:
            retweet = hasattr(tweet, 'retweeted_status')
            rows.append([tweet._json['user']['id'],
                         tweet._json['user']['screen_name'],
                         tweet._json['user']['name'],
                         tweet._json['retweet_count'],
                         tweet._json['favorite_count'],
                         tweet._json['created_at'],
                         retweet,
                         tweet._json['entities']['hashtags'],
                         tweet._json['entities']['user_mentions'],
                         tweet._json['full_text']])
        writer.writerows(rows)

# Lecture des données dans le dataframe
tweets_df = pd.read_csv(dataset_T, sep=";")

#Segmentation des tweets et retweets et création d'un DataFrame contenant les retweets
tweets_df_rt = tweets_df[tweets_df['retweeted'] == False]
retweets_df = tweets_df[tweets_df['retweeted'] == True]
reseau_df_rt = retweets_df[retweets_df['text'].str.contains("RT @")]
reseau_df_final = (reseau_df_rt.assign(rt_user = reseau_df_rt['text'].str.split('@').str[1].str.split(':').str[0])[['t_user','rt_user','user_id','retweet_count','favorite_count','created_at','retweeted','hashtags', 'user_mentions','text']])
reseau_df_final = reseau_df_final.rename(columns={'t_user': 'rt_user', 'rt_user': 't_user'})

# Creation de fichier csv
dataset_RT = datetime.datetime.now().strftime('data/dataset_RT_%m-%d-%Y.csv')
reseau_df_final.to_csv(dataset_RT,sep=";")

# Lecture des données du dataframe
reseau_df_final = pd.read_csv(dataset_RT,sep=";")

# Chargement des fichiers csv
df_list = []
for filename in glob.glob('data/dataset_RT*.csv'):
    df = pd.read_csv(filename, sep=";")
    df = df.rename(columns={'rt_user': 't_user', 't_user': 'rt_user'})
    df_list.append(df)
concat_df = pd.concat(df_list, ignore_index=True)
concat_df.to_csv('data/dataset_RT_final.csv', sep=";", index=False)
