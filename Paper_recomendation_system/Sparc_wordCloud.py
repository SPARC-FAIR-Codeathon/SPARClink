import numpy as np
import os
import re
from PIL import Image
from os import path
import nltk
import string
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

def makeImage(text):
    alice_mask = np.array(Image.open("sparc.jpg"))
    wc = WordCloud(background_color="white", max_words=1000, mask=alice_mask)
    wc.generate_from_frequencies(text)
    plt.figure(figsize = (20,20))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig("sparc1.jpg")
    plt.show()

def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def text_lowercase(text):
    return text.lower()

def get_stopwords():
    nltk.download('stopwords')

def set_stopwords():
    return set(stopwords.words('english'))

def generate_wordCloud(sentences):
    text = []
    en_stops = set_stopwords()
    for sentence in sentences:
      text.append([i for i in remove_punctuation(text_lowercase(sentence)).split(" ") if i not in en_stops])
    text = Counter([i for j in text for i in j])
    makeImage(text)

def main(sentences):
   #sentences is list of strings e.g. ["hello my name is SPARC", "SPARC link won the first prize"]
   generate_wordCloud(sentences)

if __name__ == '__main__':
    main(["hello my name is SPARC", "SPARC link won the first prize"])
