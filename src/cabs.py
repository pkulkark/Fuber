import json
import webapp2
import logging
from google.appengine.ext import db
from cabs_util import Cabs


class ListAvailableCabs(webapp2.RequestHandler):
    def get(self):
        """
        Fetch all available cabs in 5km radius of current location
        """
        self.response.headers['Content-Type'] = 'application/json'
        resp = dict(
            status='Fail',
            data=''
        )
        try:
            # get the location data from query string
            loc_data = self.request.GET
            lat = loc_data.get('latitude')
            longi = loc_data.get('longitude')
            loc = db.GeoPt(lat, longi)
            loc_list = Cabs.getcabs(loc)
            logging.info(loc_list)
            resp['status'] = "Success"
            resp['data'] = loc_list
            self.response.write(json.dumps(resp))
        except Exception as err:
            resp['status'] = "Error"
            resp['data'] = err.__str__()
            self.response.write(json.dumps(resp))
        return


class CabHandler(webapp2.RequestHandler):
    def get(self, cabid):
        """
        Fetch the details of particular cab
        """
        self.response.headers['Content-Type'] = 'application/json'
        resp = dict(
            status='Fail',
            data=''
        )
        try:
            cab_info = Cabs.getcabdetails(cabid)
            logging.info(cab_info)
            resp['status'] = "Success"
            resp['data'] = cab_info
            self.response.write(json.dumps(resp))
        except Exception as err:
            resp['status'] = "Error"
            resp['data'] = err.__str__()
            self.response.write(json.dumps(resp))

    def put(self, cabid):
        """
        Update location to new location and make cab available
        """
        self.response.headers['Content-Type'] = 'application/json'
        resp = dict(
            status='Fail',
            data=''
        )
        payload = self.request.body
        putvar = json.loads(payload)
        try:
            newlat = float(putvar['latitude'])
            newlongi = float(putvar['longitude'])
            new_loc = db.GeoPt(newlat, newlongi)
            Cabs.updatecablocation(cabid, new_loc)
            resp['status'] = "Success"
            resp['data'] = "Cab made available in new location"
            self.response.write(json.dumps(resp))
        except Exception as err:
            resp['status'] = "Error"
            resp['data'] = err.__str__()
            self.response.write(json.dumps(resp))
        return

app = webapp2.WSGIApplication([('/cabs/', ListAvailableCabs),
                               ('/cabs/(.*)', CabHandler)], debug=True)
