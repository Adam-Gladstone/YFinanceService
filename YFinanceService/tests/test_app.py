"""
Reference: https://www.digitalocean.com/community/tutorials/unit-test-in-flask

"""

import sys
import os
import pytest

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from YFinanceService.YFinanceService import app


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client


def test_version_info(client):
    """Test the version info route."""
    response = client.get('YFinanceService/VersionInfo')
    assert response.status_code == 200
    assert response.json == {"VersionInfo": {"flask": "3.1.0", "yfinance": "0.2.54", "pandas": "2.2.3"}}


def test_intrinsic_value(client):
    """ Test intrinsic value route """
    response = client.get('YFinanceService/IntrinsicValue?ticker=SAN.MC&avg_yield=3.25&cur_yield=1.25')
    assert response.status_code == 200


def test_intrinsic_value_no_params(client):
    """ Test intrinsic value route with no parameters """
    response = client.get('YFinanceService/IntrinsicValue')

    errors: dict = response.json

    assert response.status_code == 400
    assert errors['message'] == "Input payload validation failed"


def test_intrinsic_value_empty_params(client):
    """ Test intrinsic value route with an empty parameter """
    response = client.get('YFinanceService/IntrinsicValue?ticker=')

    errors: dict = response.json

    assert response.status_code == 400
    assert errors['message'] == "Input payload validation failed"


def test_intrinsic_value_incorrect_params(client):
    """ Test intrinsic value route with an incorrect parameter key """
    response = client.get('YFinanceService/IntrinsicValue?ticker=MSFT&average_yield=3.25&cur_yield=1.25')

    errors: dict = response.json

    assert response.status_code == 400
    assert errors['message'] == "Input payload validation failed"


def test_intrinsic_value_bad_ticker(client):
    """ Test intrinsic value route with a bad ticker symbol """
    response = client.get('YFinanceService/IntrinsicValue?ticker=WIBBLE&avg_yield=3.25&cur_yield=1.25')

    assert response.status_code == 200
    assert response.json == {"value": 0.0}


def test_ticker_data(client):
    """ Test ticker data route """
    response = client.get('YFinanceService/TickerData?tickers=DOC,BC,LHX&fields=trailingPE,forwardPE')

    assert response.status_code == 200
