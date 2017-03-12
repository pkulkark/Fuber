from google.appengine.ext import db
from cabs_util import CabsInfo

import webapp2


class LoadAllCabs(webapp2.RequestHandler):
    """
    Initialize the CabsInfo datatable with initial cab details
    """
    def get(self):
        cabs_details = [("C01", True, "Blue", (12.77,77.91)),
                        ("C02", True, "Pink", (12.71,77.92)),
                        ("C03", True, "Black", (12.74,77.95)),
                        ("C04", True, "White", (12.76,77.99)),
                        ("C05", True, "Pink", (12.78,77.96))]
        for each_cab in cabs_details:
            loc = each_cab[-1]
            geo_loc = db.GeoPt(loc[0], loc[1])
            cabinfo = CabsInfo(key_name=each_cab[0], Available=each_cab[1], Cabid=each_cab[0], Colour=each_cab[2], location=geo_loc)
            cabinfo.update_location()
            cabinfo.put()


app = webapp2.WSGIApplication([('/initcabs/', LoadAllCabs)], debug=True)
