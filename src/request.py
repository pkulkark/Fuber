import gpxpy.geo
import json
import logging
import webapp2
from request_util import Requests
from cabs import Cabs
from google.appengine.ext import db


class RequestHandler(webapp2.RequestHandler):
    def get(self, req_id):
        """
        Fetch status of the given request
        """
        resp = dict(
            status='Fail',
            data=''
        )
        try:
            reqstat = Requests.getrequestinfo(req_id)
            logging.info(reqstat)
            resp['status'] = "Success"
            resp['data'] = reqstat
            self.response.write(json.dumps(resp))
        except Exception as err:
            resp['status'] = "Error"
            resp['data'] = err.__str__()
            self.response.write(json.dumps(resp))

    def post(self, req_id=None):
        """
        Create new request
        """
        resp = dict(
            status='Fail',
            data=''
        )
        try:
            payload = self.request.body
            postvar = json.loads(payload)
            lat = float(postvar['latitude'])
            longi = float(postvar['longitude'])
            colour = postvar.get('colour')
            current_loc = db.GeoPt(lat, longi)
            distance_dict = {}
            ret_dict = {}
            res = Cabs.getcabs(current_loc, colour)
            if res:
                for each_cab_det in res:
                    cab_lat = each_cab_det['latitude']
                    cab_lon = each_cab_det['longitude']
                    distance = gpxpy.geo.haversine_distance(lat, longi, cab_lat, cab_lon)
                    distance_dict[distance] = each_cab_det['cabid']
                min_distance = min(distance_dict.keys())
                cabid = distance_dict[min_distance]
                cab_details = Cabs.getcabdetails(cabid)
                ret_dict['latitude'] = cab_details['latitude']
                ret_dict['longitude'] = cab_details['longitude']
                ret_dict['cabid'] = cab_details['cabid']
                logging.info(cab_details)
               # assign cab to user
                Cabs.assigncab(cabid)
               # generate request id
                new_reqid = Requests.createnewrequest()
                ret_dict['req_id'] = new_reqid
                logging.info(new_reqid)
                resp['status'] = "Success"
                resp['data'] = ret_dict
                self.response.write(json.dumps(resp))
            else:
                resp['data'] = "No cabs available"
                self.response.write(json.dumps(resp))
        except Exception as err:
            resp['status'] = "Error"
            resp['data'] = err.__str__()
            self.response.write(json.dumps(resp))
        return

    def put(self, req_id):
        """
        Change request status of given request
        """
        resp = dict(
            status='Fail',
            data=''
        )
        try:
            payload = self.request.body
            putvar = json.loads(payload)
            status = putvar['status']
            Requests.updatereqstatus(req_id, status)
            resp['status'] = "Success"
            resp['data'] = "Request status updated"
            self.response.write(json.dumps(resp))
        except Exception as err:
            resp['status'] = "Error"
            resp['data'] = err.__str__()
            self.response.write(json.dumps(resp))
        return


app = webapp2.WSGIApplication([('/requests/(.*)', RequestHandler)], debug=True)
