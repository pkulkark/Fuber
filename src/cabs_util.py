import geo.geomodel
import logging
from google.appengine.ext import db


class CabsInfo(geo.geomodel.GeoModel):
    Available = db.BooleanProperty(required=True, indexed=True)
    Cabid = db.StringProperty(required=True, indexed=True)
    Colour = db.StringProperty(required=True)


class Cabs:
    def __init__(self):
        pass

    @staticmethod
    def getcabs(loc, colour=None):
        """
        Method to get available cabs in 5km radius of the given location
        and preferred colour if any.
        :param loc: current location
        :param colour: preferred colour of cab
        :return: list fof dictionaries containing available cab details
        """
        loc_list = []
        if colour:
            avail_cabs = CabsInfo.proximity_fetch(CabsInfo.all().filter('Available =', True).filter('Colour =',colour), loc,
                                                  max_results=10,
                                                  max_distance=5000)
        else:
            avail_cabs = CabsInfo.proximity_fetch(CabsInfo.all().filter('Available =', True), loc,
                                                  max_results=10,
                                                  max_distance=5000)

        for cab in avail_cabs:
            cab_det = {}
            cab_det['cabid'] = cab.Cabid
            cab_det['latitude'] = cab.location.lat
            cab_det['longitude'] = cab.location.lon
            loc_list.append(cab_det)
        return loc_list

    @staticmethod
    def getcabdetails(cabid):
        """
        Method to get the details of a particular cab
        :param cabid: cabid of the required cab
        :return: dictionary containing details of the cab
        """
        cabkey = db.Key.from_path('CabsInfo', cabid)
        cabdetails = db.get(cabkey)
        cab_info = {}
        cab_info['cabid'] = cabdetails.Cabid
        cab_info['available'] = cabdetails.Available
        cab_info['colour'] = cabdetails.Colour
        cab_info['latitude'] = cabdetails.location.lat
        cab_info['longitude'] = cabdetails.location.lon
        return cab_info

    @staticmethod
    def updatecablocation(cabid, newloc):
        """
        Method to update the location of the given cab
        and make it available
        :param cabid: cabid of the cab
        :param newloc: new location of the cab
        """
        cabkey = db.Key.from_path('CabsInfo', cabid)
        cabdetails = db.get(cabkey)
        cabdetails.location = newloc
        cabdetails.Available = True
        cabdetails.put()
        return

    @staticmethod
    def assigncab(cabid):
        """
        Method to make cab unavailable once assigned
        :param cabid: cabid of the cab
        """
        cabkey = db.Key.from_path('CabsInfo', cabid)
        cabdetails = db.get(cabkey)
        cabdetails.Available = False
        cabdetails.put()
        return
