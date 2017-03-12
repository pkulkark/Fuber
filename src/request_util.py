import uuid
from google.appengine.ext import db


class RequestsInfo(db.Model):
    reqid = db.StringProperty(required=True, indexed=True)
    reqstatus = db.StringProperty(required=True)

class Requests:
    def __init__(self):
        pass

    @staticmethod
    def getrequestinfo(reqid):
        """
        Method to fetch the status of the given request
        :param reqid: request id of the request
        :return: status of the request
        """
        reqkey = db.Key.from_path('RequestsInfo', reqid)
        reqdetails = db.get(reqkey)
        return reqdetails.reqstatus

    @staticmethod
    def createnewrequest():
        """
        Method to create a new request
        :return: request id of the new request
        """
        req_id = str(uuid.uuid4())[:8]
        req_status = "On going"
        new_req = RequestsInfo(key_name=req_id, reqid=req_id, reqstatus=req_status)
        new_req.put()
        return req_id

    @staticmethod
    def updatereqstatus(reqid, newstatus):
        """
        Method to change the status of the given request
        :param reqid: request id of the request to be updated
        :param newstatus: new status of the request
        """
        reqkey = db.Key.from_path('RequestsInfo', reqid)
        reqdetails = db.get(reqkey)
        reqdetails.reqstatus = newstatus
        reqdetails.put()
        return