import json
import unittest
from ExternalAPIs.NIH_NCBI import NIH_NCBI

class TestNIH_NCBI(unittest.TestCase, NIH_NCBI):

    #----------------------------------------------------
    # test_NIHFundingDetailsPayload:
    # Generate POST request payloads for 2 examples in the NIH reporter API documentation.
    # Check whether our generated payload matches example in the documentatio.
    #----------------------------------------------------
    def test_NIHFundingDetailsPayload (self):
        payload = self._generateFundingDetailsPayload('5UG1HD0784*')
        self.assertEquals(payload.replace(" ", ""), '{"criteria":{"project_nums":"5UG1HD0784*"}}', msg='[ERROR] Generating payload failed.')

        payload = self._generateFundingDetailsPayload(['5UG1HD078437-07', '5R01DK102815-05'])
        self.assertEquals(payload.replace(" ", ""), '{"criteria":{"project_nums":["5UG1HD078437-07","5R01DK102815-05"]}}', msg='[ERROR] Generating payload failed.')
        return

    #----------------------------------------------------
    # test_NIHFundingDetails:
    # Check whether we get correct data. If the number of results prescribed in the meta data
    # of the request matches the actual number of results returned, this test passes.
    #----------------------------------------------------
    def test_NIHFundingDetails (self):
        proj_num = ['OT3OD025349']

        data = self.getProjectFundingDetails(proj_num)
        self.assertEquals(len(data['results']), data['meta']['total'])
        return


    #----------------------------------------------------
    # test_NIHRecord:
    # Check to see whether the generated record from the response data in 'test_response.txt'
    # is correct.
    #----------------------------------------------------
    def test_NIHRecord (self):
        with open('./tests/test_response.txt', 'r') as f:
            jsonData = json.loads(f.read())
            record = self.generateRecord(jsonData)
            
            for sub_proj in jsonData['results']:
                sub_record = record[sub_proj['project_num']]
                self.assertEquals(sub_proj['org_name'], sub_record['institute'])
                self.assertEquals(sub_proj['org_country'], sub_record['country'])
                self.assertEquals(sub_proj['award_amount'], sub_record['amount'])
                self.assertEquals(sub_proj['fiscal_year'], sub_record['year'])
                self.assertEquals(sub_proj['terms'], sub_record['keywords'])
            
        return
    
    #----------------------------------------------------
    # test_NIHPublications:
    # Check to see whether the publications retrieved from the test NIH reponse data in test_response_2.txt
    # matches the number of publications shown in the website (which is 5).
    #----------------------------------------------------
    def test_NIHPublications (self):
        with open('./tests/test_response_2.txt', 'r') as f:
            jsonData = json.loads(f.read())
            record = self.generateRecord(jsonData)

            publications = {}
            for k in record:
                item = record[k]
                pubRecord = self.getPublications(item['appl_id'])
                publications.update(pubRecord)

        
        self.assertEquals(len(publications), 5)
        return
    
    #----------------------------------------------------
    # test_PublicationsOfDatasets:
    # Check whether the publications retrieved from the NCBI eutils API for a known
    # dataset doi matches the result we found from a web search.
    #----------------------------------------------------
    def test_PublicationsOfDatasets (self):
        pubData = self.getPublicationWithSearchTerm('"10.26275/DUZ8-MQ3N"')
        self.assertEquals(len(pubData), 1)
        
        for k in pubData:
            self.assertEquals(pubData[k]['title'], 'Computational analysis of mechanical stress in colonic diverticulosis')
        return
    
    #----------------------------------------------------
    # test_getCitedBy:
    # Check whether we can retrieve citations of a given paper
    #----------------------------------------------------
    def test_getCitedBy (self):
        # Check whether we can retrieve citations of a pm_id
        records = self.getCitedBy('pm_id', '32265489')
        self.assertEquals(len(records), 1)
        for k in records:
            self.assertEquals(records[k]['title'], 'Mechanotransduction in gastrointestinal smooth muscle cells: role of mechanosensitive ion channels')

        # Check whether we can retrieve citations of a pmc_id
        records = self.getCitedBy('pmc_id', '7138845')
        self.assertEquals(len(records), 1)
        for k in records:
            self.assertEquals(records[k]['title'], 'Mechanotransduction in gastrointestinal smooth muscle cells: role of mechanosensitive ion channels')
        return


if __name__ == '__main__':
    unittest.main()