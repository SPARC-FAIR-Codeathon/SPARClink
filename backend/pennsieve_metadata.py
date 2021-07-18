# -*- coding: utf-8 -*-

## Example response
## always returned as a list of datasets

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
        'award_id': 'OT2OD025340'}, 'versionPublishedAt': '2020-10-01T15:41:57.651749Z', 
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
import boto3
import requests
import pandas as pd
from tqdm import tqdm


def get_list_of_datasets_with_metadata(list_of_datasets):
    
    # get list of datasets with awards associated with it
    url = "https://api.pennsieve.io/discover/search/records"
    querystring = {"model": "award"}
    headers = {"Accept": "application/json"}

    #test request to find out how many total datsets are present
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    response.raise_for_status()
    response = response.json()

    # get all
    querystring = {"limit": response["totalCount"], "model": "award"}
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    response.raise_for_status()
    response = response.json()
    list_of_datasets = response["records"].copy()

    url = ""
    querystring = ""
    headers = ""
    response = ""

    # get latest version of each dataset
    for item in tqdm(list_of_datasets):
        url = f"https://api.pennsieve.io/discover/datasets/{item['datasetId']}"
        headers = {"Accept": "application/json"}
        response = requests.request("GET", url, headers=headers)
        response.raise_for_status()
        response = response.json()
        item['name'] = response['name']
        item['description'] = response['description']
        item['version'] = response['version']
        item['versionPublishedAt'] = response['versionPublishedAt']
        item['datasetDOI'] = 'https://dx.doi.org/' + response['doi']
        item['tags'] = response['tags']
        item['contributors'] = response['contributors']

    # extract metadata information
    for item in tqdm(list_of_datasets):
        # get the actual dataset_description.xlsx file.
        # seems to be the best way for pandas to read
        url = "https://api.pennsieve.io/zipit/discover"
        payload = {"data": {
            "paths": ["files/dataset_description.xlsx"],
            "version": item['version'],
            "datasetId": item['datasetId']
        }}
        response = requests.request("POST", url, json=payload)
        response.raise_for_status()
        local_filename = "dataset_description.xlsx"
        totalbits = 0

        # write binary data to a file that is readable in pandas
        if response.status_code == 200:
            with open(local_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        totalbits += 1024
                        # print("Downloaded",totalbits*1025,"KB...")
                        f.write(chunk)

            # only reading through xlsx files at the moment.
            # could be extended for json and csv (rare instances by SPARC curation standards) if time permits
            try:
                xl = pd.ExcelFile("dataset_description.xlsx")
                df = xl.parse("Sheet1")

                # arrays to hold dois for each dataset
                originating_article_array = []
                protocol_array = []

                # get all dois from dataframe
                for index, row in df.iterrows():
                    row_val = row['Metadata element']
                    if (row_val.find('Originating Article') != -1):
                        count = 0
                        for col_val in row:
                            if (count > 2):
                                try:
                                    if col_val.find('doi.org') != -1:
                                        pos = col_val.find('http')
                                        if pos != -1:
                                            col_val = col_val[pos:]
                                        originating_article_array.append(
                                            col_val)
                                except:
                                    pass
                            count = count + 1
                    if (row_val.find('Protocol') != -1):
                        count = 0
                        for col_val in row:
                            if (count > 2):
                                try:
                                    if (col_val.find('doi.org') != -1):
                                        pos = col_val.find('http')
                                        if pos != -1:
                                            col_val = col_val[pos:]
                                        protocol_array.append(col_val)
                                except:
                                    pass
                            count = count + 1
                item["originatingArticleDOI"] = originating_article_array
                item["protocolsDOI"] = protocol_array
            except:
                # for any xlsx files that are corrupted or cannot be read, ignore
                item["originatingArticleDOI"] = []
                item["protocolsDOI"] = []

    return list_of_datasets

datset_list = []
datset_list = get_list_of_datasets_with_metadata(list_of_datasets)
print(datset_list)
