# SPARC Search and Recommender

# Contents:
* [Description](#Description)
* [Requirement](#Requirement)
* [Steps for Usage](#Steps-for-Usage)
* [Demo](#Demo)
* [References](#References)

## Description:
This is a recommendation system that was built with the aim to make searching for documents using keywords simpler and user friendly. The two mechanisms used in this module are explained below. 

First is a word recommendation or spelling recommendation which takes a given string looks for the most probable word in the vocabulary. 

The second part uses the spelling recommendation to look for publications and datasets present in the Firebase real-time daatabase to get most relatable articles with respect to the search terms. This is based on a word embedding generated using a word2vec model (the code also provides option of using GloVe embedding). 

Word2vec model generates a vocabulary and vector representation for each article based on their title and description. When a string is serched its vector representation is generated and the cosine similarity between that vector and the vector representation of each article title/description is measured.

We pick the top 10 of these to show on the frontend.

For further reading please refer to references.

## Requirement:
To run this function standalone follow the instructions below. These commands are already handled if you are using the SPARClink conda environment.
```python
!python -m nltk.downloader stopwords
!python -m pip install -U symspellpy
!pip install --upgrade gensim
```

## Steps for usage:
The main function takes three inputs: 
1. `string`: This parameter takes in a string. The output from the search bar goes here.
2. `full_model`: If 'True' then uses Glove model. (Read below for further instructions)
3. `recommendation`: If `True` then use the word2vec model to return the article recomendation system.


```python
SparcSearch(string, full_model = False, recomendation = True)
```

Returns the publication and dataset ids in order of relevance to search field (empty list in case of `recommendation = False`) and spelling recommendation.
1. To switch off the recommendation system for papers set `recommendation` to `False`. This will then only run the spelling recommendation. 

2. If `recommendation = True` the code will perform spelling recommendation followed by paper recommendation.

3. To train the model using the Glove dataset :
   1. Download https://nlp.stanford.edu/data/glove.6B.zip 
   2. `!unzip glove.6B.zip`
   3. `get_glove2wv()`
   4. Set `full_model` to True

3. To run the code only on the words and tags associated with the dataset keep full model = Flase


## Demo:
```
python Sparcsearch.py "Identification of peripheral neural cercuit" False True
```
## References:
