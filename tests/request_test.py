from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

import json
import unittest
import sys
sys.path.append('C:\Users\Pooja Kulkarni\Fuber\src')
from request_util import RequestsInfo, Requests


class RequestsTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(
            probability=0)
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)

        #put sample data
        reqinfo = RequestsInfo(key_name="c1df2386", reqid="c1df2386", reqstatus="On going")
        reqinfo.put()

    def tearDown(self):
        self.testbed.deactivate()

    def testCreateNewReq(self):
        new_reqid = Requests.createnewrequest()
        req_stat = Requests.getrequestinfo(new_reqid)
        self.assertEqual(req_stat, "On going")

    def testGetRequest(self):
        req_id = "c1df2386"
        reqstat = Requests.getrequestinfo(req_id)
        self.assertEqual(reqstat, "On going")

    def testUpdateReqStatus(self):
        req_id = "c1df2386"
        reqstat = Requests.getrequestinfo(req_id)
        self.assertEqual(reqstat, "On going")
        new_status = "Complete"
        Requests.updatereqstatus(req_id, new_status)
        reqstat = Requests.getrequestinfo(req_id)
        self.assertEqual(reqstat, "Complete")