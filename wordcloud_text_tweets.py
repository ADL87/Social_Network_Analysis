import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import re
import nltk
nltk.download('stopwords')

# Chargement du fichier CSV
df = pd.read_csv("data/dataset_RT_final.csv", sep=";", header=0)

# Prétraitement du contenu de la colonne de "text"
def clean_text(text):
    # Exclusion des URL
    text = re.sub(r'http\S+', '', text)
    # Exclusion des notions RT
    text = re.sub(r'^RT[\s]+', '', text)
    # Exclusion des mentions @
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)
    # Exclusion des émoticônes et autres caractères spéciaux
    text = re.sub(r'[\W_]+', ' ', text, flags=re.UNICODE)
    # Exclusion des espaces
    text = text.strip()
    return text

df['text_clean'] = df['text'].apply(clean_text)

# Retrait des stopwords
stop_words = set(nltk.corpus.stopwords.words('french'))

def remove_stopwords(text):
    tokens = text.split()
    tokens_clean = [token for token in tokens if token.lower() not in stop_words]
    return " ".join(tokens_clean)

df['text_clean'] = df['text_clean'].apply(remove_stopwords)

# Génération du nuage de mots-clés
wordcloud = WordCloud(width=800, height=800, background_color='white', stopwords=STOPWORDS, collocations=False, min_font_size=10).generate(' '.join(df['text_clean']))

# Visualisation du nuage de mots-clés
import matplotlib.pyplot as plt
plt.figure(figsize=(8,8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
