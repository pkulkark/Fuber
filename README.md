Fuber
======

Fuber is an on-call taxi service hosted on Google App Engine.

Webapp2 framework is used to expose the functionality through REST APIs. The application uses app engine's datastore to store the details of cabs and user requests.

The current features of Fuber include:
 + fetch all available cabs in the vicinity,
 + fetch details of a particular cab,
 + update the location of a particular cab and make it available,
 + create a new request for cab,
 + fetch the status of a particular request,
 + update the status of a particular request.


Getting Started
===============

A running application exists on:

https://my-project1-153906.appspot.com

To deploy the application in a different project, clone the repository and
refer to the guide below:

https://cloud.google.com/appengine/docs/standard/python/getting-started/deploying-the-application


REST API Specification
======================

In the following sections you will find the specification of all URIs defined and examples on how to use them

### Available Cabs

**URI:** /cabs/?latitude=*lat*&longitude=*lon*

**Methods:**

* **GET**: Retrieve all available cabs within 5km radius of the given location

For example:

Run the curl command
```
$ curl -k -u root -H "Content-Type: application/json" -X GET 'https://my-project1-153906.appspot.com/cabs/?latitude=12.72&longitude=77.92'
```
which returns the output
```
{"status": "Success", "data": [{"latitude": 12.710000000000001, "cabid": "C02", "longitude": 77.920000000000002}, {"latitude": 12.73, "cabid": "C03", "longitude": 77.939999999999998}]}
```

### Cab Details

**URI:** /cabs/*cabid*

**Methods:**

* **GET**: Retrieve the details of the particular cab containing the cabid

For example:

The curl command
```
$ curl -k -u root -H "Content-Type: application/json" -X GET 'https://my-project1-153906.appspot.com/cabs/C02'
```
returns the output
```
{"status": "Success", "data": {"available": true, "latitude": 12.71, "colour": "Pink", "cabid": "C02", "longitude": 77.92}}
```

* **PUT**: Update the location of the cab and make cab available

For example:

The curl command
```
$ curl -k -u root -H "Content-Type: application/json" -X PUT -d '{"latitude":"12.73", "longitude":"77.95"}' 'https://my-project1-153906.appspot.com/cabs/C02'
```
returns the output
```
{"status": "Success", "data": "Cab made available in new location"}
```

### User Requests

**URI:** /requests/*reqid*

**Methods:**

* **GET**: Retrieve the details of the particular request

For example:

The curl command
```
$ curl -k -u root -H "Content-Type: application/json" -X GET 'https://my-project1-153906.appspot.com/requests/289a0ce1'
```
returns the output
```
{"status": "Success", "data": "Complete"}
```

* **POST**: Create a new request for cab at the current location and preferred colour, if any

For example:

The curl command
```
$ curl -k -u root -H "Content-Type: application/json" -X POST -d '{"latitude":"12.71","longitude":"77.92","colour":"Pink"}' 'https://my-project1-153906.appspot.com/requests/'
```
returns the output
```
{"status": "Success", "data": {"latitude": 12.710000000000001, "cabid": "C02", "req_id": "1973b136", "longitude": 77.920000000000002}}
```

* **PUT**: Update the status of a particular request

For example:

The curl command
```
$ curl -k -u root -H "Content-Type: application/json" -X PUT -d '{"status":"Complete"}' 'https://my-project1-153906.appspot.com/requests/1973b136'
```
returns the output
```
{"status": "Success", "data": "Request status updated"}
```

Unit Tests
==========
To run the unit tests, execute the following command from Google Cloud SDK Shell:

```
$ cd tests\
$ python runner.py <Google SDK Path>
```
The output should be as below:
```
testAssignCab (cabs_test.CabsTest) ... ok
testCabsListing (cabs_test.CabsTest) ... ok
testGetCabDetails (cabs_test.CabsTest) ... ok
testUpdateCabLocation (cabs_test.CabsTest) ... ok
testCreateNewReq (request_test.RequestsTest) ... ok
testGetRequest (request_test.RequestsTest) ... ok
testUpdateReqStatus (request_test.RequestsTest) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.096s

OK
```

