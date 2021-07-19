<br/> <br/>

<p align="center">
  <a href="https://github.com/SPARC-FAIR-Codeathon/SPARClink">
    <img src="https://github.com/SPARC-FAIR-Codeathon/SPARClink/blob/main/docs/images/logo.svg" alt="SPARC link logo" height="150">
  </a>
  <br/>
  <p align="center"> 
    <strong>
      Visualizing the Impact of SPARC
    </strong>
  </p>
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
    <img src="https://img.shields.io/github/repo-size/SPARC-FAIR-Codeathon/SPARClink" alt="GitHub repo size">
  </a>
  <br/> 
</p>


## What is SPARClink
### NIH SPARC
The NIH Common Fund’s Stimulating Peripheral Activity to Relieve Conditions (SPARC) program aims to transform our understanding of nerve-organ interactions with the intent of advancing bioelectronic medicine towards treatments that change lives. [Learn more about SPARC](https://sparc.science/)
### FAIR Data
By employing a [FAIR](https://www.nature.com/articles/sdata201618) (Findable, Accessible, Interoperable and Reusable) first approach SPARC datasets, protocols and publications generated via the SPARC program is intended to be able to be used by researchers globally with reproducible results. However, at the current moment, there is no real tangible way to show or visualize the usage of SPARC data in outside projects and publications. 
### Goal
The goal of SPARClink is to provide a system that will query all external publications using open source tools and platforms and create an interactable visualization that is helpful to any regular person to showcase the impact that SPARC has on the overall scientific research community. These impact measurements are meant to be used as a showcase of the concept of FAIR data and how good data generation practices and methods are useful in advancing the field of bioelectronic medicine. 

## How it works
Metadata information is extracted from [Pennsieve](https://app.pennsieve.io/), and the SPARC Airtable database. This information is queried against the [NIH Reporter](https://api.reporter.nih.gov/) and [Google Scholar](https://serpapi.com/google-scholar-api) to extract citations and create a well connected graph using [d3.js](https://d3js.org/). 

<p align="center">
  <img src="https://user-images.githubusercontent.com/21206996/125478715-d5f83b6f-8a6d-4ef8-a845-952baa27d8da.png" />
  <br/>
  <span> SPARClink workflow </span>
</p>

## Origin Story
The SPARClink project was first born as an idea at the 2021 NIH SPARC Codeathon ([More details here](https://sparc.science/help/2021-sparc-fair-codeathon)). The idea behind the topic was created as a method of visualizing citation data on datasets, protocols and publications to determine the degree of use of SPARC material outside of the official channels

## Run the project
The development environment uses Anaconda to keep track of the python dependencies. Download Anaconda here: [Anaconda Individual Edition](https://www.anaconda.com/products/individual)

``` bash
git clone https://github.com/SPARC-FAIR-Codeathon/SPARClink.git
cd SPARClink
conda env create -f environment.yml
conda activate sparclink

## Run the backend python server
cd backend
python api.py

## Run the front end
cd frontend
npm install
```


Keep track of the project [here](https://github.com/SPARC-FAIR-Codeathon/SPARClink/projects/1)

## Created by 
* [Sanjay Soundarajan](https://github.com/megasanjay)
* [Monalisa Achalla](https://github.com/a-monalisa)
* [Jongchan Kim](https://github.com/Kim-Jongchan)
* [Ashutosh Singh](https://github.com/Ashutosh1712)
* [Sachira Kuruppu](https://github.com/rsachira-abi)
