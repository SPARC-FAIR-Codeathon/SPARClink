# -*- coding: utf-8 -*-

## Example response
## always returned as a list of datasets
# originating article is the paper associated with the dataset. 

'''
[..., {
    'datasetId': 64, 
    'version': 4, 
    'name': 'Quantified Morphology of the Pig Vagus Nerve'
    'model': 'award', 
    "description": "This dataset contains recordings of compound nerve action potentials from the pelvic nerve as well as the pudendal nerves and its branches in response to electrical stimulation on the epidural surface of the sacral spinal cord in anesthetized cats.",
    'properties': {
        'description': 'Experiments to map physiological functions of autonomic nerves and the continued advance of bioelectronictherapies are limited by inadequate activation or block of targeted nerve fibers and unwanted co-activation orblock of non-targeted nerve fibers. More fundamentally, the relationship between applied stimuli and the nervefibers that are activated or blocked, how this relationship varies across individuals and species, and how theserelationships can be controlled remain largely unknown. We will develop, implement and validate an efficientcomputational pipeline for simulation of electrical activation and block of different nerve fiber types withinautonomic nerves. The pipeline will include segmentation of microanatomy from fixed nerve samples, three-dimensional finite-element models of electrodes positioned on nerves, and non-linear cable models of differentnerve fiber types, enabling calculation of quantitative input-output maps of activation and block of specific nervefibers. As key benchmarks of pipeline development and for the proposed analysis and design efforts, we willimplement models of the cervical (VNc) and abdominal (VNa) vagus nerves in rat, in a SPARC-identified animalmodel, and in human. The VNc is an excellent test bed as it contains a broad spectrum of nerve fiber types,there are experimental data to facilitate model validation, and there are multiple applications of VNc stimulationwhere a lack of fiber selectivity limits the therapeutic window. The VNa is an excellent complement to the cervicalVNc, as a prototypical autonomic nerve of a size comparable to many of the small autonomic nerves targetedby SPARC projects. We will use the models that emerge from the pipeline to achieve analysis and design goalsto address critical gaps identified as SPARC priorities. Specifically, we will quantify of the effects of intra-speciesdifferences in nerve morphology on activation and block by building individual sample-specific models for eachnerve and specie. These models will also be used to quantify inter-species differences in nerve fiber activationand block and to identify electrode designs and stimulation parameters that produce equivalent degrees ofactivation and block across species. We will combine the resulting models with engineering optimization todesign approaches to increase the selectivity and efficiency of activation and block of different nerve fiber types.The outcomes will be a pipeline for modeling autonomic nerves, electrode geometries, and stimulationparameters, as well as tools that address the limitations of nerve stimulation selectivity and efficiency that hinderthe continued advance of physiological mapping studies and the development of bioelectronic therapies.', 
        'id': 'db090035-8a57-4474-8c3d-2536dee9499f', 
        'principal_investigator': 'GRILL, WARREN M.', 
        'title': 'MODELING ACTIVATION AND BLOCK OF AUTONOMIC NERVES FOR ANALYSIS AND DESIGN', 
        'award_id': 'OT2OD025340'}, 
    'versionPublishedAt': '2020-10-01T15:41:57.651749Z', 
    'datasetDOI': 'https://dx.doi.org/10.26275/maq2-eii4', 
    'tags': [
        'vagus nerve stimulation', 
        'neural anatomy', 
        'vagus nerve morphology', 
        'autonomic nervous system'], 
    'contributors': [
        {'firstName': 'Nicole', 'middleInitial': 'A', 'lastName': 'Pelot', 'degree': 'Ph.D.', 'orcid': '0000-0003-2844-0190'}, 
        {'firstName': 'Gabriel', 'middleInitial': 'B', 'lastName': 'Goldhagen', 'degree': None, 'orcid': None}, 
        {'firstName': 'Jake', 'middleInitial': 'E', 'lastName': 'Cariello', 'degree': None, 'orcid': None}, 
        {'firstName': 'Warren', 'middleInitial': 'M', 'lastName': 'Grill', 'degree': 'Ph.D.', 'orcid': '0000-0001-5240-6588'}], 
    'originatingArticleDOI': [], 
    'protocolsDOI': ['dx.doi.org/10.17504/protocols.io.6bvhan6']}, ...]
'''


### Import required python modules
from serpapi import GoogleSearch
import pandas as pd

# Function that takes originatingArticleDOI scaraped from Pennsieve as input and searches

def get_fromoriginatingdoi(originatingArticleDOI, authorization_key):
    params = {
        "engine": "google_scholar",
        "q": originatingArticleDOI,
        "api_key": authorization_key
    }
    search = GoogleSearch(params)
    results = search.get_json()
    return results

# results = get_fromoriginatingdoi("10.13003/5jchdy")
# output below
'''
{
    'organic_results': [
        ..., 
        {
            'inline_links': {
                'cached_page_link': 'http://scholar.googleusercontent.com/scholar?q=cache:38JRjgMPVNUJ:scholar.google.com/+10.13003/5jchdy&hl=en&as_sdt=0,44',
                'cited_by': {
                    'cites_id': '15371927936069386975',
                    'link': 'https://scholar.google.com/scholar?cites=15371927936069386975&as_sdt=5,44&sciodt=0,44&hl=en',
                    'serpapi_scholar_link': 'https://serpapi.com/search.json?as_sdt=5%2C44&cites=15371927936069386975&engine=google_scholar&hl=en',
                    'total': 4
                },
                'related_pages_link': 'https://scholar.google.com/scholar?q=related:38JRjgMPVNUJ:scholar.google.com/&scioq=10.13003/5jchdy&hl=en&as_sdt=0,44',
                'serpapi_cite_link': 'https://serpapi.com/search.json?engine=google_scholar_cite&q=38JRjgMPVNUJ'
            },
            'link': 'http://ceur-ws.org/Vol-2821/paper2.pdf',
            'position': 0,
            'publication_info': {
                'authors': [
                    {
                        'author_id': 'ZJExJkAAAAAJ',
                        'link': 'https://scholar.google.com/citations?user=ZJExJkAAAAAJ&hl=en&oi=sra',
                        'name': 'LC Gleim',
                        'serpapi_scholar_link': 'https://serpapi.com/search.json?author_id=ZJExJkAAAAAJ&engine=google_scholar_author&hl=en'
                    },
                    {
                        'author_id': 'uhVkSswAAAAJ',
                        'link': 'https://scholar.google.com/citations?user=uhVkSswAAAAJ&hl=en&oi=sra',
                        'name': 'S Decker',
                        'serpapi_scholar_link': 'https://serpapi.com/search.json?author_id=uhVkSswAAAAJ&engine=google_scholar_author&hl=en'
                    }],
                    'summary': 'LC Gleim, S Decker - MEPDaW@ ISWC, 2020 - ceur-ws.org'
                },
            'resources': [
                {
                    'file_format': 'PDF',
                    'link': 'http://ceur-ws.org/Vol-2821/paper2.pdf',
                    'title': 'ceur-ws.org'
                }],
            'result_id': '38JRjgMPVNUJ',
            'snippet': '… RFC 3986 (2005) 2. Crossref Display Guidelines (2017), https://doi.org/10.13003/5jchdy 3. Gleim, L., Pennekamp, J., et al.: FactDAG: Formalizing Data Interoperability in an Internet of Production. IEEE Internet of Things Journal pp …',
            'title': 'Timestamped URLs as Persistent Identifiers.',
            'type': 'Pdf'
        }, 
        ...],
    'search_information': {
        'organic_results_state': 'Results for exact spelling',
        'query_displayed': '10.13003/5jchdy',
        'time_taken_displayed': 0.02,
        'total_results': 4
    },
    'search_metadata': {
        'created_at': '2021-07-18 18:32:46 UTC',
        'google_scholar_url': 'https://scholar.google.com/scholar?q=10.13003%2F5jchdy&hl=en',
        'id': '60f473cee135080701bee081',
        'json_endpoint': 'https://serpapi.com/searches/51e7edffa34ec3a5/60f473cee135080701bee081.json',
        'processed_at': '2021-07-18 18:32:46 UTC',
        'raw_html_file': 'https://serpapi.com/searches/51e7edffa34ec3a5/60f473cee135080701bee081.html',
        'status': 'Success',
        'total_time_taken': 2.65
    },
    'search_parameters': {'engine': 'google_scholar',
    'hl': 'en',
    'q': '10.13003/5jchdy'
    }
}

'''


# Taking publication information and citation information from scraped data
def getcitationandpubinfo(results):
  record = {}
  for item in results['organic_results']:
    data = {}
    data['title'] = item['title']
    data['author_info'] = item['publication_info']
    data['citation_info'] = item['inline_links']
    data['cites_id'] = item['inline_links']['cited_by']['cites_id']
    record[item['position']] = data
    return record


#response = getcitationandpubinfo(results)

# response is shown below
'''
{
    0: {
        'author_info': {
            'authors': [
                {
                    'author_id': 'ZJExJkAAAAAJ',
                    'link': 'https://scholar.google.com/citations?user=ZJExJkAAAAAJ&hl=en&oi=sra',
                    'name': 'LC Gleim',
                    'serpapi_scholar_link': 'https://serpapi.com/search.json?author_id=ZJExJkAAAAAJ&engine=google_scholar_author&hl=en'
                },
                {
                    'author_id': 'uhVkSswAAAAJ',
                    'link': 'https://scholar.google.com/citations?user=uhVkSswAAAAJ&hl=en&oi=sra',
                    'name': 'S Decker',
                    'serpapi_scholar_link': 'https://serpapi.com/search.json?author_id=uhVkSswAAAAJ&engine=google_scholar_author&hl=en'
                }],
            'summary': 'LC Gleim, S Decker - MEPDaW@ ISWC, 2020 - ceur-ws.org'
            },
        'citation_info': {
            'cached_page_link': 'http://scholar.googleusercontent.com/scholar?q=cache:38JRjgMPVNUJ:scholar.google.com/+10.13003/5jchdy&hl=en&as_sdt=0,44',
            'cited_by': {
                'cites_id': '15371927936069386975',
                'link': 'https://scholar.google.com/scholar?cites=15371927936069386975&as_sdt=5,44&sciodt=0,44&hl=en',
                'serpapi_scholar_link': 'https://serpapi.com/search.json?as_sdt=5%2C44&cites=15371927936069386975&engine=google_scholar&hl=en',
                'total': 4
            },
            'related_pages_link': 'https://scholar.google.com/scholar?q=related:38JRjgMPVNUJ:scholar.google.com/&scioq=10.13003/5jchdy&hl=en&as_sdt=0,44',
            'serpapi_cite_link': 'https://serpapi.com/search.json?engine=google_scholar_cite&q=38JRjgMPVNUJ'
        },
        'cites_id': '15371927936069386975',
        'title': 'Timestamped URLs as Persistent Identifiers.'
    },
    1: {
        'author_info': {
            'summary': 'НН Литвинова - Наука и научная информация, 2020 - neiconjournal.com'
        },
        'citation_info': {
            'cached_page_link': 'https://scholar.googleusercontent.com/scholar?q=cache:jz7zw7flARgJ:scholar.google.com/+10.13003/5jchdy&hl=en&as_sdt=0,44',
            'cited_by': {
                'cites_id': '1729916309316255375',
                'link': 'https://scholar.google.com/scholar?cites=1729916309316255375&as_sdt=5,44&sciodt=0,44&hl=en',
                'serpapi_scholar_link': 'https://serpapi.com/search.json?as_sdt=5%2C44&cites=1729916309316255375&engine=google_scholar&hl=en',
                'total': 1
            },
            'html_version': 'https://www.neiconjournal.com/jour/article/view/91',
            'related_pages_link': 'https://scholar.google.com/scholar?q=related:jz7zw7flARgJ:scholar.google.com/&scioq=10.13003/5jchdy&hl=en&as_sdt=0,44',
            'serpapi_cite_link': 'https://serpapi.com/search.json?engine=google_scholar_cite&q=jz7zw7flARgJ',
            'versions': {
                'cluster_id': '1729916309316255375',
                'link': 'https://scholar.google.com/scholar?cluster=1729916309316255375&hl=en&as_sdt=0,44',
                'serpapi_scholar_link': 'https://serpapi.com/search.json?as_sdt=0%2C44&cluster=1729916309316255375&engine=google_scholar&hl=en',
                'total': 3
            }
        },
        'cites_id': '1729916309316255375',
        'title': 'Многоликий DOI CrossRef: все ли функции мы используем?'
    },
}
'''

# Function to use cites_id and search all related items
def get_fromcitesid(cites_id, authorization_key):
    params = {
        "engine": "google_scholar",
        "cites": cites_id,
        "api_key": authorization_key
    }
    search = GoogleSearch(params)
    results = search.get_json()
    return results
