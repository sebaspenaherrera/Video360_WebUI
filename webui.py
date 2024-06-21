'''
Summary: This script defines the FastAPI server and mounts the Dash app as a sub-application.
This module is responsible for compatibility between FastAPI and Dash (WSGI), and for defining the main API endpoint.
'''

from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.responses import RedirectResponse
from monitoring_app import app as monitoring


# Define the FastAPI server
app = FastAPI()
# Mount the Dash app as a sub-application in the FastAPI server
app.mount("/monitoring/", WSGIMiddleware(monitoring.server))


# Define the main API endpoint
@app.get("/")
def index():
    # Redirect to another route
    return RedirectResponse(url="/monitoring/")