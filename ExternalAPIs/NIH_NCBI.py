#-----------------------------------------------------------------------------
# NIH_NCBI.py:
# API to acquire data from NIH reporter and NCBI eutils
#
# Author: Sachira Kuruppu
# Date  : 16/07/2021
#-----------------------------------------------------------------------------

import time
import json
import requests
import urllib.parse as urlparser
from requests.structures import CaseInsensitiveDict

class NIH_NCBI:

    __NIH_timestamp = None  # can post only 1 request per second
    __NCBI_timestamp = None # can post only 3 requests per second

    #----------------------------------------------------
    # __maintainRequestFrequency:
    # This function maintains the request frequency specified by the API providers by
    # pausing the execution.
    #----------------------------------------------------
    def __maintainRequestFrequency (self, timestamp, request_per_second):
        seconds_per_request = 1 / request_per_second
        if (timestamp != None):
            dt = time.time() - timestamp
            if (dt < seconds_per_request):
                time.sleep(seconds_per_request - dt)
        return time.time()

    #----------------------------------------------------
    # _generateFundingDetailsPayload:
    # Given a project number, this private function generates a POST payload to be 
    # sent to the NIH reporter.
    #----------------------------------------------------
    def _generateFundingDetailsPayload (self, project_no):
        data = {}
        data['criteria'] = {'project_nums': project_no}
        return json.dumps(data)
    
    #----------------------------------------------------
    # _generateNCBIpublicationRecord:
    # Generate a publication record from the json data retrieved from NCBI eutils
    #----------------------------------------------------
    def _generateNCBIpublicationRecord (self, jsonPub):
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
    # _getPublicationFromPubmed:
    # Retrieve information about a publication using pm_id from NCBI eutils
    #----------------------------------------------------
    def _getPublicationFromPubmed (self, pm_id):
        self.__NCBI_timestamp = self.__maintainRequestFrequency(self.__NCBI_timestamp, 3)
        resp = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=' + str(pm_id))

        record = {}
        if (resp.status_code == 200):
            jsonData = json.loads(resp.content)
            record = self.__generateNCBIpublicationRecord(jsonData['result'][str(pm_id)])
            if 'doi' not in record:
                record['doi'] = pm_id # We use the doi as the key. This will help debug publications without doi

        return record

    #----------------------------------------------------
    # _getPublicationFromPMC:
    # Retrieve information about a publication from PMC using the pmc_id from NCBI eutils
    #----------------------------------------------------
    def _getPublicationFromPMC (self, pmc_id):
        self.__NCBI_timestamp = self.__maintainRequestFrequency(self.__NCBI_timestamp, 3)
        resp = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pmc&retmode=json&id=' + str(pmc_id))
        
        record = {}
        if (resp.status_code == 200):
            jsonData = json.loads(resp.content)
            record = self._generateNCBIpublicationRecord(jsonData['result'][str(pmc_id)])
            if 'doi' not in record:
                record['doi'] = pmc_id #We use the doi as the key. This will help debug publicastions without doi
        
        return record
    
    #----------------------------------------------------
    # getProjectFundingDetails:
    # This function retrieves data from NIH reporter for a given project identified by
    # the 'project_no'.
    # project_no = [List of project numbers]
    #----------------------------------------------------
    def getProjectFundingDetails (self, project_no):
        self.__NIH_timestamp = self.__maintainRequestFrequency(self.__NIH_timestamp, 1)
        url = "https://api.reporter.nih.gov/v1/projects/Search/"
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"

        payload = self._generateFundingDetailsPayload(project_no)
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
        self.__NIH_timestamp = self.__maintainRequestFrequency(self.__NIH_timestamp, 1)
        resp = requests.get('https://reporter.nih.gov/services/Projects/Publications?projectId=' + str(appl_id))
        
        record = {}
        if (resp.status_code == 200):
            jsonPub = json.loads(resp.content)
            
            for pub in jsonPub['results']:
                pubmed_data  = self._getPublicationFromPubmed(pub['pm_id'])

                data = {}
                data['title']   = pub['pub_title']
                data['authors'] = pub['author_list']
                data['journal'] = pub['journal_title']
                data['year']    = pub['pub_year']
                data['url']     = pub['journal_title_link']['value']

                record[pubmed_data['doi']] = data
                
        
        return record

    #----------------------------------------------------
    # getPublicationsOfDataset:
    # Use NCBI API to retrieve publications that mention the dataset identified by
    # the doi. This function assumes that all the papers that mention the given doi
    # uses the dataset.
    #----------------------------------------------------
    def getPublicationsOfDataset (self, doi):
        self.__NCBI_timestamp = self.__maintainRequestFrequency(self.__NCBI_timestamp, 3)
        term = urlparser.quote('"' + str(doi) + '"', safe='')
        resp = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&retmode=json&term=' + term)

        record = {}
        if (resp.status_code == 200):
            jsonData = json.loads(resp.content)
            pmc_ids = jsonData['esearchresult']['idlist']

            for pmc_id in pmc_ids:
               pub = self._getPublicationFromPMC(pmc_id)
               record[pub['doi']] = pub

        return record
    