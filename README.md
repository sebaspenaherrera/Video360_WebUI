# 360-Video User Interface (UI)
This UI is designed for data monitoring for 360-Video service. This web server is based on a REST API that constantly 
updates the values from a remote service. This latter service should be hosted by another REST Server reachable by this 
service.
The data REST server is continuously receiving data from the HMD, which MUST be configured in DEMO MODE, this way, this
server can request data samples through HTTP GET operations.
