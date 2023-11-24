import uvicorn
from config_params import *
from web_server import app as monitoring
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware


# Define the FastAPI server
app = FastAPI()
# Mount the Dash app as a sub-application in the FastAPI server
app.mount("/monitoring/", WSGIMiddleware(monitoring.server))


# Define the main API endpoint
@app.get("/")
def index():
    return "Hello"


if __name__ == "__main__":

    # Run the rest API app using Uvicorn with the parameters in config_parameters file
    uvicorn.run(app="main:app", port=web_port, host=web_host, reload=web_reload)
