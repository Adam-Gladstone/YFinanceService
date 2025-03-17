"""
    Test stock valuation function
"""

import sys
import os
import pytest

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from YFinanceService.YFinanceService import app
from resources.finance_data import stock_valuation


@pytest.fixture
def client():
    """ Set up a test client for the app. """
    with app.test_client() as client:
        yield client


def test_valuation(client):
    """ Test stock valuation using Graham's formula """

    symbol = "SAN.MC"
    average_yield: float = 4.4
    current_yield: float = 1.25

    v: float = stock_valuation(symbol, average_yield, current_yield)

    # No value
    assert v != 0.0
