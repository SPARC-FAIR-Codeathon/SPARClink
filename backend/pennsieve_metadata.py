# -*- coding: utf-8 -*-

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
