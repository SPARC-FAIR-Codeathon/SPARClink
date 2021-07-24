import re, os
from collections import Counter
from symspellpy.symspellpy import SymSpell as SymSpellPy, Verbosity
from gensim.models import Word2Vec
from collections import Counter
from sklearn.datasets import fetch_20newsgroups
import re
import nltk
import string
from nltk.corpus import stopwords
from gensim.test.utils import datapath
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import requests as req
import json


class SpellCheck:
    def __init__(self, dictionary=None, verbose=0):
        self.verbose = verbose
        self.dictionary = dictionary
        
    def correction(self, text):
        return ''

class SpellCorrector(SpellCheck):
    def __init__(self, dictionary, verbose=0):
        super().__init__(dictionary=dictionary, verbose=verbose)

    def words(text):
        return re.findall(r'\w+', text.lower())

    def P(self, word): 
        "Probability of `word`."
        N = sum(self.dictionary.values())
        return self.dictionary[word] / N

    def correction(self, word): 
        "Most probable spelling correction for word."
        return max(self.candidates(word), key=self.P)

    def candidates(self, word, verbose=0): 
        "Generate possible spelling corrections for word."
        
        known_result = self.known([word])
        edit1_result = self.known(self.edits1(word))
        edit2_result = self.known(self.edits2(word))
        
        if self.verbose > 0 or verbose > 0:
            print('Known Result: ', known_result)
            print('Edit1 Result: ', edit1_result)
            print('Edit2 Result: ', edit2_result)
        
        return (known_result or edit1_result or edit2_result or [word])

    def known(self, words):
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.dictionary)

    def edits1(self, word):
        "All edits that are one edit away from `word`."
        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word): 
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))
    
    
class SymSpell(SpellCheck):
    def __init__(self, dictionary_file_path='', dictionary=None, verbose=0):
        super().__init__(dictionary=dictionary, verbose=verbose)
        
        self.dictionary_file_path = dictionary_file_path
        self.model = None
        
    def load_vocab(self, corpus_file_path, max_edit_distance_dictionary=2, prefix_length=5):
        #initial_capacity = len(corpus)
        
        #sym_spell = SymSpellPy(
        #    initial_capacity, max_edit_distance_dictionary, 
        #    prefix_length)
        self.model = SymSpellPy(
            max_dictionary_edit_distance=max_edit_distance_dictionary, 
            prefix_length=prefix_length)

        term_index = 0  # column of the term in the dictionary text file
        count_index = 1  # column of the term frequency in the dictionary text file
        if not self.model.load_dictionary(corpus_file_path, term_index, count_index):
            print("Dictionary file not found")
        
    def build_vocab(self, dictionary, file_dir, file_name, verbose=0):
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        """
            Data format:
                token, frequency
            Example:
                edward 154
                edwards 50
                ...
        """ 
        if self.verbose > 3 or verbose > 3:
            print('Size of dictionary: %d' % len(dictionary))

        with open(file_dir + file_name, "w") as text_file:
            for token, count in dictionary.items():
                text_file.write(token + ' ' + str(count))
                text_file.write('\n')
        
    def correction(self, word, max_edit_distance_lookup=2, mode='cloest'): 
        if mode == 'cloest':
            suggestion_verbosity = Verbosity.CLOSEST
        elif mode == 'top':
            suggestion_verbosity = Verbosity.TOP
        elif mode == 'all':
            suggestion_verbosity = Verbosity.ALL
              
        results = self.model.lookup(
            word, suggestion_verbosity, max_edit_distance_lookup)
        
        results = [{'word': suggestion.term, 'count': suggestion.count, 'distance': suggestion.distance} for suggestion in results]
        return results
    
    def corrections(self, sentence, max_edit_distance_lookup=2):
        normalized_sentence = (sentence.lower())
        results = self.model.lookup_compound(
            normalized_sentence, max_edit_distance_lookup)
        
        results = [{'word': suggestion.term, 'distance': suggestion.distance} for suggestion in results]
        return results

def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)
def text_lowercase(text):
    return text.lower()

def generate_model_our_Data(title):
    # define training data
    sentences = title
    # train model
    model = Word2Vec(sentences, min_count=1)
    # summarize the loaded model
    print(model)
    # summarize vocabulary
    words = list(model.wv.key_to_index)
    print(words)
    # save model
    model.save('model_short.bin')

    new_model = Word2Vec.load('model_short.bin')
    return new_model

def get_glove2wv():
    glove_input_file = '/content/glove.6B.100d.txt'
    word2vec_output_file = 'glove.6B.100d.txt.word2vec'
    glove2word2vec(glove_input_file, word2vec_output_file)
    filename = '/content/glove.6B.100d.txt.word2vec'
    model = KeyedVectors.load_word2vec_format(filename, binary=False)

def work_with_glove(new_model):
    filename = '/content/glove.6B.100d.txt.word2vec'
    model = KeyedVectors.load_word2vec_format(filename, binary=False)
    model.add_vectors(list(new_model.wv.key_to_index), new_model.wv.get_normed_vectors())
    return model 

def run_spellrecomender(title_word = False):
    corpus = []
    for line in fetch_20newsgroups().data:
        line = line.replace('\n', ' ').replace('\t', ' ').lower()
        line = re.sub('[^a-z ]', ' ', line)
        tokens = line.split(' ')
        tokens = [token for token in tokens if len(token) > 0]
        corpus.extend(tokens)
    corpus = Counter(corpus)
    corpus_dir = '../../data/'
    corpus_file_name = 'spell_check_dictionary.txt'
    if title_word:
        corpus = title_word
    symspell = SymSpell(verbose=10)
    symspell.build_vocab(dictionary=corpus, file_dir=corpus_dir, file_name=corpus_file_name)
    symspell.load_vocab(corpus_file_path=corpus_dir+corpus_file_name)
    return symspell
  
def check_spell(symspell, w):
    results = symspell.correction(word= w)
    return results
  
def get_title_word_freq_dict(title):
    title_word = [i for k in title for i in k]
    return Counter(title_word)

def create_titleandlookup(dataset_df):
    title = []
    lookup = []
    en_stops = set_stopwrds()
    for i in dat3["Papers"]:
      if "title" in dat3["Papers"][i]:
        title.append([i for i in remove_punctuation(text_lowercase(dat3["Papers"][i]["title"])).split(" ") if i not in en_stops])
        lookup.append(i)
    for i in dat3["Datasets"]:
        ret = [remove_punctuation(text_lowercase(dat3["Datasets"][i]["name"])).split(" "), dat3["Datasets"][i]["tags"], remove_punctuation(text_lowercase(dat3["Datasets"][i]["description"])).split(" ") ]
        ret = [i for j in ret for i in j]
        ret = [i for i in ret if i not in en_stops]
        title.append(ret)
        lookup.append(i)
    return title, lookup

def get_stopwords():
    nltk.download('stopwords')

def set_stopwrds():
    return set(stopwords.words('english'))

def find_recomendation( title, lookup, word_list, new_model):
    distance = []
    for i in title:
      distance.append(new_model.wmdistance(word_list, i))
    if list(set(distance))[0] == np.inf:
      return "not in the vocablary"
    else:
      zipped_lists = zip(distance, lookup)
      sorted_zipped_lists = sorted(zipped_lists)
      sorted_list1 = [element for _, element in sorted_zipped_lists]
    return sorted_list1

def getRecomendation(string, dat3):
    string = remove_punctuation(text_lowercase(string)).split(" ")
    title, lookup = create_titleandlookup(dat3)
    symspell = run_spellrecomender(get_title_word_freq_dict(title))
    correct_spell = []
    for i in string:
        correct_spell.append(check_spell(symspell, i)[0]["word"])
    print(correct_spell)
    new_model = generate_model_our_Data(correct_spell)
    new_model = work_with_glove(new_model)
    fr = find_recomendation( title, lookup, correct_spell, new_model)
    return fr

def main(string):
    response = req.get("https://sparclink-f151d-default-rtdb.firebaseio.com/.json")
    dataset = response.json()
    dat3 = dataset["ikP4sIT5PJMWFNCKG5eof5RN2Em1"]
    json_string = json.dumps(getRecomendation(string, dat3))
    with open('data.json', 'w') as jsonfile:
         json.dump(json_string, jsonfile)
    

if __name__ == '__main__':
    main("Identification of peripheral neural cercuit")
    
