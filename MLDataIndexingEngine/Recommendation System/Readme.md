# Spelling and Paper Recomender

# Contents:
* [Description](#Description)
* [Requirement]
* [Steps for Usage]
* [Demo]
* [References]

## Description:
Sparcsearch.py is a recomendation system that was built with the aim to make serching for documents using keywords simpler and user friendly. There are two mechanism here. First one is a word recomendation or spelling recomendation which given a string tries to look for the most probable word in the vocabulary. The second part uses the spelling recomendation to look for papers and dataset present in the firebase dataset to get most relatable articles to whats being searched. This is based on the word embedding generated using word2vec model (the code also provides option of using GloVe embedding). Word2vec model generates a vabulary and vector representation for each article based on their title and description. when a string is serched it's vector represtenation is generated and then we measure the cosine similarity between that vector and the vector representation of each article title/description. We pick the top 10 of these to show on the website.
For further reading please refer to references.
## Requirement:
To use this function as a standalone (outside this website) follow the below instruction otherwise these are also mentioned in environmoent of this website
```
!python -m nltk.downloader stopwords
```
```
!python -m pip install -U symspellpy
```
```
!pip install --upgrade gensim
```
## Steps for usage:
The main function takes three inputs: 
1. `string` This paprameter takes in a string. The output from the search bar goes here.
2. `full_model` If 'True' then uses Glove model. (Read below for further instruction)
3. `recomendation` If `True` then use the word2vec model to return the article recomendation system.
```
main(string, full_model = False, recomendation = True)
```
Returns the paper and dataset ids in order of relevance to search field (empty list in case of `recomendation = False`) and spelling recomendation.
1. To switch off the recomendation system for papers -> `recomendation = False`
   This will then just perform spelling recomendation. If `recomendation = True` the code will perform spelling recomendation followed by paper recomendation.

2. To train the model using Glove dataset :
   1. Download https://nlp.stanford.edu/data/glove.6B.zip 
   2. `!unzip glove.6B.zip`
   3. `get_glove2wv()`
   4. Set full_model = True

3. To run the code only on the words and tags associated with the dataset keep full model = Flase


## Demo:
```
python Sparcsearch.py "Identification of peripheral neural cercuit" False True
```
## References:
