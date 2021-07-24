# Spelling and Paper Recomender

## Requirement:
```
!python -m nltk.downloader stopwords
```
```
!python -m pip install -U symspellpy
```
```
!pip install --upgrade gensim
```
## Demo
```
python Sparcsearch.py("Identification of peripheral neural cercuit",False, True)
```
## Steps for usage:
The main function takes three inputs: 
string, full_model = False, recomendation = True
Returns the paper and dataset ids in order of relevance to search field (empty list in case of recomendation -> False) and spelling recomendation.
1. To switch off the recomendation system for papers -> recomendation = False
   This will then just perform spelling recomendation. If recomendation = True the code will perform spelling recomendation followed by paper recomendation.

2. To train the model using Glove dataset :
   a. Download https://nlp.stanford.edu/data/glove.6B.zip 
   b. `!unzip glove.6B.zip`
   c. `get_glove2wv()`
   d. Set full_model = True

3. To run the code only on the words and tags associated with the dataset keep full model = Flase
