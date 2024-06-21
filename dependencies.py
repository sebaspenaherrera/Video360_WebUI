'''
Define all the dependencies that will be used in the project. Planed to be deprecated in the future
'''

##################################
#               Utils
##################################
import time
from datetime import datetime
import os
import json
import base64
import numpy as np
import pandas as pd
import requests
import traceback
##################################
#               DASH
##################################
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash_daq import Slider


##################################
#               PLOTLY
##################################
import plotly.graph_objs as go
import plotly.express as px  # (version 4.7.0)
import io
import plotly.graph_objects as go
##################################
#               UVICORN
##################################
from fastapi import FastAPI, Query, Path, Body
from typing import Union, Annotated
import pandas as pd

