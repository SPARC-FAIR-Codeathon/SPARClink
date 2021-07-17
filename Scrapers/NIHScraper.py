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
        else:
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
            data['institute'] = sub_project['org_name']
            data['country']   = sub_project['org_country']
            data['amount']    = sub_project['award_amount']
            data['year']      = sub_project['fiscal_year']
            data['keywords']  = sub_project['terms']

            record[sub_project['project_num']] = data
        return record