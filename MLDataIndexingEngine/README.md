# ML Data Indexing Engine

This module is used to run additional analytics on the search terms for a more smarter SPARClink experience. There are three submodules in this section that references the three key features that are used by SPARClink.

## Keyword Extraction
content here

## SPARC Search
content here

## Word Cloud
This mmodule is used to generate a list of keywords for the word map visualization that is shown in the left control panel. The api recieves a list of sentences and  analyzes the content before suggesting the best list of keywords ranked in descending order. On the front end we use the top 20 terms returned to generate the interactive wordcloud. 

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
