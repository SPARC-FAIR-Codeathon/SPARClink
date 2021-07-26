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

The second part uses the spelling recommendation to look for publications and datasets present in the Firebase real-time daatabase to get most relatable articles with respect to the search terms. This is based on a word embedding generated using a word2vec model. GloVe is an unsupervised algorithm that attempts to obtain high-dimensional vector representations of words using global word-word co-occurrence. This has been shown to encode interesting semantic information and to encode semantically related words nearby one another. (the code also provides option of using GloVe embedding). 

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
```python Sparcsearch.py "neoral cercuit" False True```
```python
output :
['103389fnins201900897',
  '101016jtins202009011',
  '101016jconb201911011',
  '1014797FVDN2224',
  '101016jneuron202007010',
  '101093europaceeuy134',
  '101038s41593-021-00828-2',
  '101016jconb201804006',
  '101007s10827-019-00709-5',
  '101038s41587-019-0198-8',
  '101038s41586-020-2474-7',
  '101038s41586-021-03413-6',
  '103389fncel201800469',
  '101210endocrbqab087',
  '101016jexpneurol2020113256',
  '101002mds27321',
  '103389fphys2020563372',
  'https:dxdoiorg1026275yo5c-etlo',
  '101016jcell201705034',
  '101152ajpheart006352019',
  'https:dxdoiorg1026275yum2-z4uf',
  'https:dxdoiorg1026275eyik-qjhm',
  '101128IAI00928-19',
  '101523JNEUROSCI2158-192020',
  'https:dxdoiorg1026275dv4h-izxs',
  '101186s42234-019-0030-2',
  '101016jneuron202009031',
  '101038s41575-020-0271-2',
  '101016jjacc201910046',
  '101016jconb201712011',
  'https:dxdoiorg1026275dn1d-owj9',
  'https:dxdoiorg1026275iprt-7m5c',
  'https:dxdoiorg1026275dqpf-gqdt',
  'https:dxdoiorg1026275higx-q8hs',
  'https:dxdoiorg1026275uxjv-kbrz',
  '101152jn004422020',
  'https:dxdoiorg1026275zpju-kpjd',
  '101016jcell202005029',
  '103389fnins2020619275',
  '101523JNEUROSCI0743-192019',
  '101016jomtm202102012',
  '101146annurev-cancerbio-030419-033413',
  ...]
```
Top 15 paper titles :

```python
A Student’s Guide to Neural Circuit Tracing
Neural Circuits of Interoception
Parenting — a paradigm for investigating the neural circuit basis of behavior
Neural Mechanisms and Therapeutic Opportunities for Atrial Fibrillation
Viral vectors for neural circuit mapping and recent advances in trans-synaptic anterograde tracers
Neural ablation to treat ventricular arrhythmias
An amygdala-to-hypothalamus circuit for social reward
The neural circuits of thermal perception
Emerging techniques in statistical analysis of neural data.
Next-generation interfaces for studying neural function
Microbes modulate sympathetic neurons via a gut-brain circuit
An amygdala circuit that suppresses social engagement.
Methods for Three-Dimensional All-Optical Manipulation of Neural Circuits
The Effects of Estrogens on Neural Circuits That Control Temperature
Targeted activation of spinal respiratory neural circuits
...
```
```
## References:
1. For Symspell look below:
    1. https://github.com/wolfgarbe/symspell
    2. https://wolfgarbe.medium.com/1000x-faster-spelling-correction-algorithm-2012-8701fcd87a5f
2. [GloVe](https://nlp.stanford.edu/projects/glove/)
