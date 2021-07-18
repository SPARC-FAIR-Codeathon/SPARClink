#-----------------------------------------------------------------------------
# NIHScraper.py:
# API to acquire data from NIH reporter
#
# Author: Sachira Kuruppu
# Date  : 16/07/2021
#-----------------------------------------------------------------------------

import json
import requests
from requests.structures import CaseInsensitiveDict

from bs4 import BeautifulSoup

class NIHScraper:

    #----------------------------------------------------
    # __generateFundingDetailsPayload:
    # Given a project number, this private function generates a POST payload to be 
    # sent to the NIH reporter.
    #----------------------------------------------------
    def __generateFundingDetailsPayload (self, project_no):
        data = {}
        data['criteria'] = {'project_nums': project_no}
        return json.dumps(data)
    
    #----------------------------------------------------
    # __generateNCBIpublicationRecord:
    # Generate a publication record from the json data retrieved from NCBI eutils
    #----------------------------------------------------
    def __generateNCBIpublicationRecord (self, jsonPub):
        data = {}

        data['title'] = jsonPub['title']
        data['jounal'] = jsonPub['source']
        data['year'] = jsonPub['pubdate'].split(' ')[0]

        author_list = ''
        for author in jsonPub['authors']:
            author_list = author['name'] + ', '
        data['author_list'] = author_list

        for id in jsonPub['articleids']:
            data[id['idtype']] = id['value']

        return data

    #----------------------------------------------------
    # __getPublicationFromPubmed:
    # Retrieve information about a publication using pm_id from NCBI eutils
    #----------------------------------------------------
    def __getPublicationFromPubmed (self, pm_id):
        resp = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=' + str(pm_id))

        record = {}
        if (resp.status_code == 200):
            jsonData = json.loads(resp.content)
            record = self.__generateNCBIpublicationRecord(jsonData['result'][str(pm_id)])

        return record

    #----------------------------------------------------
    # __getPublicationFromPMC:
    # Retrieve information about a publication from PMC using the pmc_id from NCBI eutils
    #----------------------------------------------------
    def __getPublicationFromPMC (self, pmc_id):
        resp = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pmc&retmode=json&id=' + str(pmc_id))
        
        record = {}
        if (resp.status_code == 200):
            jsonData = json.loads(resp.content)
            record = self.__generateNCBIpublicationRecord(jsonData['result'][str(pmc_id)])
        return record
    
    #----------------------------------------------------
    # getProjectFundingDetails:
    # This function retrieves data from NIH reporter for a given project identified by
    # the 'project_no'.
    # project_no = [List of project numbers]
    #----------------------------------------------------
    def getProjectFundingDetails (self, project_no):
        url = "https://api.reporter.nih.gov/v1/projects/Search/"
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"

        payload = self.__generateFundingDetailsPayload(project_no)
        resp = requests.post(url, headers=headers, data=payload)
        
        if (resp.status_code == 200):
            return json.loads(resp.content)
        
        return {}

    #----------------------------------------------------
    # generateRecord:
    # Given the json object containing the data recevied from NIH reporter,
    # this function generates a dict containing only the important fields, that has to be
    # stored in the central database.
    #----------------------------------------------------
    def generateRecord (self, jsonData):
        record = {}

        for sub_project in jsonData['results']:
            data = {}
            data['appl_id']   = sub_project['appl_id']
            data['institute'] = sub_project['org_name']
            data['country']   = sub_project['org_country']
            data['amount']    = sub_project['award_amount']
            data['year']      = sub_project['fiscal_year']
            data['keywords']  = sub_project['terms']

            record[sub_project['project_num']] = data
        return record
    
    #----------------------------------------------------
    # getPublications:
    # Retrieve publications associated witha given grant application identified by the "appl_id"
    #----------------------------------------------------
    def getPublications (self, appl_id):
        resp = requests.get('https://reporter.nih.gov/services/Projects/Publications?projectId=' + str(appl_id))
        
        record = {}
        if (resp.status_code == 200):
            jsonPub = json.loads(resp.content)
            
            for pub in jsonPub['results']:
                doi  = self.__getPublicationDOI(pub['pm_id'])

                data = {}
                data['title']   = pub['pub_title']
                data['authors'] = pub['author_list']
                data['journal'] = pub['journal_title']
                data['year']    = pub['pub_year']
                data['url']     = pub['journal_title_link']['value']

                record[doi] = data
                
        
        return record

    #----------------------------------------------------
    # getPublicationsOfDataset:
    # Use NCBI API to retrieve publications that mention the dataset identified by
    # the doi. This function assumes that all the papers that mention the given doi
    # uses the dataset.
    #----------------------------------------------------
    def getPublicationsOfDataset (self, doi):
        resp = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&retmode=json&term=' + str(doi))

        record = {}
        if (resp.status_code == 200):
            jsonData = json.loads(resp.content)
            pmc_ids = jsonData['esearchresult']['idlist']

            for pmc_id in pmc_ids:
               pub = self.__getPublicationFromPMC(pmc_id)
               record[pub['doi']] = pub

        return record
    