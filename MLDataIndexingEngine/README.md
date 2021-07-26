# ML Data Indexing Engine

This module is used to run additional analytics on the search terms for a more smarter SPARClink experience. There are three submodules in this section that references the three key features that are used by SPARClink.

## Keyword Extraction
This module is used to generate keyword using keyBERT pretrained model. It generates top 50 key words associated with the whole document. It also make use of Maximal marginal relevence algorithm to pick key words that have higher distance among them. This is to ensure diversity among the choosen key words.

## SPARC Search
This module is primarily used for the Top 10 recommended related items in the bottom left panel. Filter keywords are passed to the function via a https request and the server will return a list of most relevant publications, protocols and datasets. The second query parameter is used for the smart filter feature that can be found in the [`smart_filter`](https://github.com/SPARC-FAIR-Codeathon/SPARClink/tree/smart_filter) branch. A list of what we think is the right word is returned in the response.

```javascript
var axios = require('axios');
var data = JSON.stringify({
  "inputString": "Identification of peripheral neural cercuit",
  "fullModel": false,
  "recommendation": true
});

var config = {
  method: 'post',
  url: 'https://megasanjay.pythonanywhere.com/sparcsearch',
  headers: { 
    'Content-Type': 'application/json'
  },
  data : data
};

axios(config)
.then(function (response) {
  console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});

```

## Word Cloud
This module is used to generate a list of keywords for the word map visualization that is shown in the left control panel. The api recieves a list of sentences and  analyzes the content before suggesting the list of best keywords ranked in descending order. On the front end we use the top 20 terms returned to generate the interactive wordcloud. 

```javascript
var axios = require('axios');
var data = JSON.stringify({
  "sentences": [
    "Annotated heart scaffold for pig available for registration of segmented neural anatomical-functional mapping of cardiac neural circuits.",
    "Data from the innervation of intact mice hearts and the mapping of parasympathetic and sympathetic neural circuits which control heart rate. This data set identifies the cholinergic and noradrenergic neurons which project to the sinoatrial node."
  ]
});

var config = {
  method: 'post',
  url: 'https://megasanjay.pythonanywhere.com/wordcloud',
  headers: { 
    'Content-Type': 'application/json'
  },
  data : data
};

axios(config)
.then(function (response) {
  console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});
```
