from google.appengine.ext import testbed
from google.appengine.ext import db
from google.appengine.datastore import datastore_stub_util

import unittest
import webapp2
import webtest
import json
import sys
sys.path.append('C:\Users\Pooja Kulkarni\Fuber\src')
from cabs_util import Cabs, CabsInfo
from cabs import ListAvailableCabs, CabHandler


class CabsTest(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication([('/cabs', ListAvailableCabs),
                                       ('/cabs/(.*)', CabHandler)])
        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(
            probability=0)
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)

        #put sample data
        cabinfo = CabsInfo(key_name="C02", Available=True, Cabid="C02", Colour="Black", location=db.GeoPt(12.71,77.93))
        cabinfo.update_location()
        cabinfo.put()

    def tearDown(self):
        self.testbed.deactivate()

    def testCabsListing(self):
        lat = 12.72
        lon = 77.92
        query_string = '?latitude='+str(lat)+'&longitude='+str(lon)
        resp = self.testapp.get('/cabs'+query_string)
        resp = json.loads(resp.normal_body)
        self.assertEqual("Success", resp['status'])

    def testGetCabDetails(self):
        cab_id = 'C02'
        cab_det = Cabs.getcabdetails(cab_id)
        self.assertEqual(cab_det['cabid'], cab_id)
        self.assertEqual(cab_det['available'], True)
        self.assertEqual(cab_det['colour'], "Black")

    def testUpdateCabLocation(self):
        cab_id = 'C02'
        lat = 12.77
        lon = 77.95
        new_loc = db.GeoPt(lat, lon)
        cab_det = Cabs.getcabdetails(cab_id)
        self.assertEqual(cab_det['latitude'], 12.71)
        self.assertEqual(cab_det['longitude'], 77.93)
        Cabs.updatecablocation(cab_id, new_loc)
        cab_det = Cabs.getcabdetails(cab_id)
        self.assertEqual(cab_det['latitude'], lat)
        self.assertEqual(cab_det['longitude'], lon)

    def testAssignCab(self):
        cab_id = 'C02'
        Cabs.assigncab(cab_id)
        cab_det = Cabs.getcabdetails(cab_id)
        self.assertEqual(cab_det['available'],False)




