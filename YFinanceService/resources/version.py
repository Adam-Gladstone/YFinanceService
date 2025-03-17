from importlib.metadata import version
from flask import Flask
from flask_restx import Resource

import pandas as pd
import yfinance as yf


class VersionInfo(Resource):
    def get(self):
        """ API to retrieve version info from underlying components """

        vi: dict = {}

        vi["flask"] = version('flask')
        vi["yfinance"] = yf.__version__
        vi["pandas"] = pd.__version__

        return {"VersionInfo": vi}, 200  # return info and 200 OK code
