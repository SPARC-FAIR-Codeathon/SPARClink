<br/> <br/>

<p align="center">
  <a href="https://github.com/SPARC-FAIR-Codeathon/SPARClink">
    <img src="https://github.com/SPARC-FAIR-Codeathon/SPARClink/blob/main/docs/images/logo.svg" alt="SPARC link logo" height="150">
  </a>
  <br/>
  <h3 align="center">
    Visualizing the Impact of SPARC
  </h3>
</p>

<p align="center">
  <a href="https://github.com/SPARC-FAIR-Codeathon/SPARClink/blob/main/LICENSE" alt="GitHub license">
    <img src="https://img.shields.io/github/license/SPARC-FAIR-Codeathon/SPARClink" />
  </a>
  <a href="https://github.com/SPARC-FAIR-Codeathon/SPARClink/stargazers" alt="GitHub stars">
    <img src="https://img.shields.io/github/stars/SPARC-FAIR-Codeathon/SPARClink" />
  </a>
  <a href="https://github.com/SPARC-FAIR-Codeathon/SPARClink/network" alt="GitHub forks">
    <img src="https://img.shields.io/github/forks/SPARC-FAIR-Codeathon/SPARClink" />
  </a>
  <a href="https://github.com/SPARC-FAIR-Codeathon/SPARClink/issues" alt="GitHub issues">
    <img src="https://img.shields.io/github/issues/SPARC-FAIR-Codeathon/SPARClink" />
  </a>
  <a href="https://github.com/SPARC-FAIR-Codeathon/SPARClink/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/SPARC-FAIR-Codeathon/SPARClink" alt="GitHub contributors">
  </a>
  <a href="#">
    <img src="https://img.shields.io/github/last-commit/SPARC-FAIR-Codeathon/SPARClink" alt="GitHub last commit">
  </a>
  <a href="#">
    <img src="https://img.shields.io/tokei/lines/github/SPARC-FAIR-Codeathon/SPARClink" alt="Lines of code">
  </a>
  <a href="#">
    <img src="https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github" alt="Open Source? Yes!">
  </a>
  <br/> 
</p>

<h4 align="center">
  <a href="https://sparclink-f151d.web.app/sparclink" target="_blank">SPARClink Web App</a>
</h4>
 <br/> <br/>
<p align="center">
  <img src="https://github.com/SPARC-FAIR-Codeathon/SPARClink/blob/main/docs/images/2021-07-25%2013-47-30.gif"/>
</p>
<br/> <br/>
 
 
## Table of content
- [What is SPARClink?](#what-is-sparclink)
  - [NIH SPARC](#nih-sparc)
  - [FAIR Data](#fair-data)
  - [Defining Impact](#defining-impact)
  - [Origin Story](#origin-story)
  - [Goal](#goal)
- [How it works](#how-it-works)
- [Run the project](#run-the-project)
  - [Testing](#testing)
  - [Firebase Backend Implementation](#firebase-backend-implementation)
  - [Visualization Web App](#visualization-web-app)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)
- [Further Reading](#further-reading)

## What is SPARClink?
### NIH SPARC
The NIH Common Fund’s Stimulating Peripheral Activity to Relieve Conditions (SPARC) program aims to transform our understanding of nerve-organ interactions with the intent of advancing bioelectronic medicine towards treatments that change lives. [Learn more about SPARC](https://sparc.science/about)

### FAIR Data
By employing a [FAIR](https://www.nature.com/articles/sdata201618) (Findable, Accessible, Interoperable and Reusable) first approach SPARC datasets, protocols and publications generated via the SPARC program is intended to be able to be used by researchers globally with reproducible results. However, at the current moment, there is no real tangible way to show or visualize the usage of SPARC data in outside projects and publications. 

### Origin Story
The SPARClink project was first born as an idea at the 2021 NIH SPARC Codeathon ([more details here](https://sparc.science/help/2021-sparc-fair-codeathon)). The idea behind the topic was created as a method of visualizing citation data on datasets, protocols and publications to determine the degree of use of SPARC material outside of the official channels.

### Defining Impact
The word 'Impact' can have many different meanings depending on the context that it is viewed in. Within the SPARClink project, we consider impact to be the frequency of citations of SPARC funded resources. The SPARC program intends to advance medical understanding by providing datasets, maps and computational studies that follow FAIR principles and is used by researchers all around the world. The usage of SPARC resouces by platforms and programs ouside SPARC is what we view as the meaning of the term 'Impact'.

### Goal
The goal of SPARClink is to provide a system that will query all external publications using open source tools and platforms and create an interactable visualization that is helpful to any person (researcher or otherwise) to showcase the impact that SPARC has on the overall scientific research community. These impact measurements are meant to be used as a showcase of the concept of FAIR data and how good data generation practices and methods are useful in advancing the field of bioelectronic medicine.

However, datasets and protocols are not referenced similar to prior research in manuscripts. Dataset and protocol identifiers or urls are only mentioned in text or under supplementary materials, making this a difficult task to accomplish.

## How it works?
Metadata information on datasets and protocols are extracted from [Pennsieve](https://app.pennsieve.io/), SPARC Airtable database, and [Protocols.io](https://www.protocols.io/workspaces/sparc). This information is queried against the [NIH RePORTER](https://api.reporter.nih.gov/), [NCBI](https://www.ncbi.nlm.nih.gov/), and [Google Scholar](https://serpapi.com/google-scholar-api) to extract citations and create a well connected graph using [d3.js](https://d3js.org/). 

<p align="center">
  <!--<img src="https://user-images.githubusercontent.com/21206996/125478715-d5f83b6f-8a6d-4ef8-a845-952baa27d8da.png" />-->
  <img src="https://github.com/SPARC-FAIR-Codeathon/SPARClink/blob/main/docs/images/sparclink_block_diagram-01.png" width="500"/>
  <br/>
  <span> SPARClink workflow </span>
</p>

## Run the project
Clone or download the repository.
``` bash
git clone https://github.com/SPARC-FAIR-Codeathon/SPARClink.git
```

The development environment uses [Anaconda](https://www.anaconda.com/products/individual) to keep track of the python dependencies. Download Anaconda here: [Anaconda Individual Edition](https://www.anaconda.com/products/individual).

The following would create a new `conda` environment with the dependencies required to run the project.
``` bash
cd SPARClink
conda env create -f environment.yml --prefix ./env 
conda activate ./env
```
The application uses [python-dotenv](https://github.com/theskumar/python-dotenv) to load configuration information from a `.env` file. Create a `.env` file with the following information.
``` bash
PROTOCOLS_IO_KEY="<protocols.io api key>"
SERPAPI_KEY="<serpapi api key>"
```
A public API key for protocols.io can be obtained by signing up as [shown here](https://www.protocols.io/developers). SERP api key is not required at the moment. To integrate google scholar results, an API key can be obtained as [shown here](https://serpapi.com/).

### Testing
Unit tests to verify external APIs are written in Python unittest framework. The tests can be run as shown below:
``` bash
python -m unittest -v tests/test_NIH_NCBI.py
```

### Firebase Backend Implementation
Currently, the central database is implemented as a [Firebase](https://firebase.google.com/) real-time database. The database can be updated by running `FirebaseImplementation.py`. However, this requires a username and a password.

To use your own Firebase instance, setup a Firebase web app as [shown here](https://firebase.google.com/docs/web/setup), and update `firebaseConfig` in `FirebaseImplementation.py` with the new API keys. [Setup a new user](https://firebase.google.com/docs/auth/web/password-auth), and configure the [real-time database](https://firebase.google.com/docs/database/web/start). It is recommended to limit the database write permission to authenticated users. Run `FireabaseImplementation.py` and enter user's email/password when prompted.

<p align="center">
  <!--<img src="https://user-images.githubusercontent.com/21206996/125478715-d5f83b6f-8a6d-4ef8-a845-952baa27d8da.png" />-->
  <img src="https://github.com/SPARC-FAIR-Codeathon/SPARClink/blob/main/docs/images/backend_flow_chart-01.png" width="500"/>
  <br/>
  <span>Backend Flow Chart: Shows the methods implemented in the backend to gather citations of datasets, protocols, and SPARC publications.</span>
</p>

### ML Data Indexing Engine
We have setup a [Flask](https://flask.palletsprojects.com/en/2.0.x/) server on [pythonanywhere](https://www.pythonanywhere.com/) to handle all our machine learning operations. If you would like to setup a backend for your own fork, please setup a flask server on any hosting service of your choice and modify the approriate endpoints in the `flask_app.py` file. To learn more about the techniques we used, refer to the [Further Reading](https://github.com/SPARC-FAIR-Codeathon/SPARClink#further-reading) section. 

### Visualization Web App
The vizualizations created from the realtime database can be viewed directly from our [demo page](https://sparclink-f151d.web.app/sparclink) or by running the local version of our frontend. We use [Vue.js](https://vuejs.org/) and [Tailwind CSS](https://tailwindcss.com/) to render the demo webpage. The interactive force directed graph is created via [d3.js](https://d3js.org/) using data requested from our Firebase real-time database. Within the SPARClink demo page we use the HTML canvas element to render the visualization. In order to get your forked repo frontend to run locally, use the following commands:
```bash
cd frontend
npm install
npm run serve
```
You can now open your browser and visit the url [http://localhost:8080/sparclink](http://localhost:8080/sparclink) to view the webpage. 


`Note:` To use the smart word filter, please refer to the frontend available in the [`smart_filter`](https://github.com/SPARC-FAIR-Codeathon/SPARClink/tree/smart_filter/frontend) branch. This feature will lead to slower render times on the graph visualization so we have not included it in the main branch.

<p align="center">
  <img src="https://github.com/SPARC-FAIR-Codeathon/SPARClink/blob/main/docs/images/2021-07-25 14-44-36.gif" />
  <br/>
  <span> SPARClink smart filter </span>
</p>

<!--Keep track of the project [here](https://github.com/SPARC-FAIR-Codeathon/SPARClink/projects/1)-->

## Maintainers
* [Sanjay Soundarajan](https://github.com/megasanjay)
* [Monalisa Achalla](https://github.com/a-monalisa)
* [Jongchan Kim](https://github.com/Kim-Jongchan)
* [Ashutosh Singh](https://github.com/Ashutosh1712)
* [Sachira Kuruppu](https://github.com/rsachira-abi)

## Contributing
If you would like to suggest an idea to this project, please let us know in the [issues](https://github.com/SPARC-FAIR-Codeathon/SPARClink/issues) page and we will take a look at your suggestion. Please use the `enhacement` tag to label your suggestion. 

If you would like to add your own feature, feel free to fork the project and send a pull request our way. This is an open source project so we will welcome your contributiobs with open arms. 
Refer to our [Contributing Guildeines](./docs/CONTRIBUTING.md) and [Code of Conduct](./docs/CODE_OF_CONDUCT.md) for more information. Add a [GitHub Star](https://github.com/SPARC-FAIR-Codeathon/SPARClink) to support active development!

## License
SPARClink is an open source project and distributed under the  MIT License. See [LICENSE](./LICENSE) for more details.

## Further Reading
- [External APIs](./ExternalAPIs/README.md)
- [SPARC APIs](./SPARC/README.md)
- [Visualization and frontend](./frontend/README.md)
- [ML Data Indexing Engine](./MLDataIndexingEngine/README.md)
