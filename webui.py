from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.responses import RedirectResponse
from monitoring_app import app as monitoring

print("He cargado esto")
# Define the FastAPI server
app = FastAPI()
# Mount the Dash app as a sub-application in the FastAPI server
app.mount("/monitoring/", WSGIMiddleware(monitoring.server))


# Define the main API endpoint
@app.get("/")
def index():
    # Redirect to another route
    return RedirectResponse(url="/monitoring/")