from flask_restx import Resource, reqparse

import pandas as pd
import yfinance as yf
import yahoo_fin.stock_info as si

from resources.valuation import stock_valuation_graham


def get_value(info: dict, key: str):
    """
        Retrieve a value from a ticker info dictionary
        or None if the key doesn't exist
    """

    if info is not None:
        if key in info.keys():
            return info[key]

    return None


def get_items(symbol: str, fields: list) -> list:
    """
        Retrieve data from the corresponding fields for the specified ticker
    """

    items: list = [symbol]

    try:
        tk: dict = yf.Ticker(symbol)
        info: dict = tk.info

        for field in fields:
            items.append(get_value(info, field))
    except Exception:
        pass

    return items


def stock_valuation(symbol: str, avg_yield: float, cur_yield: float) -> float:
    """
        Call the stock_valuation_graham function with the specified inputs.
    """

    v: float = 0.0

    try:
        ticker = yf.Ticker(symbol)

        if ticker is None:
            return v

        info: dict = ticker.info
        if info is None:
            return v

        # EPS = earnings per share (over the trailing twelve months (TTM))
        eps: float = info["trailingEps"]

        # 8.5 = price-to-earnings (P/E) base for a no-growth company
        pe_base: float = 8.5

        # g = reasonably expected annual growth rate (over the next 7-10 years)
        # For next five year growth estimates use the yahoo finance
        # stock info library
        valuation: pd.DataFrame = si.get_stats_valuation(symbol)
        projected_growth: str = valuation.loc[4, "Current"]
        g: float = float(projected_growth)

        v: float = stock_valuation_graham(eps, pe_base, g, avg_yield, cur_yield)

    except Exception:
        v: float = 0.0

    return v


class TickerInfo(Resource):
    """ Retrieve a complete dictionary of the ticker info. """
    def get(self):

        parser = reqparse.RequestParser()

        parser.add_argument(
            "ticker", type=str, required=True, help="The ticker symbol of the stock"
        )

        args = parser.parse_args()

        symbol: str = args.get("ticker")

        tk: dict = yf.Ticker(symbol)

        return {"data": tk.info}, 200  # return info and 200 OK code


class TickerData(Resource):
    """ Retrieve the specified fields from the input tickers """
    def get(self):

        parser = reqparse.RequestParser()

        parser.add_argument(
            "tickers", type=str, action='split', required=True, help="One or more ticker symbols"
        )

        parser.add_argument(
            "fields", type=str, action='split', required=True, help="One or more fields"
        )

        args = parser.parse_args()

        symbols: list = args.get("tickers")
        fields: list = args.get("fields")

        headers: list = ['Ticker']
        for field in fields:
            headers.append(field)

        rows: list = []

        try:

            for symbol in symbols:
                rows.append(get_items(symbol, fields))

        except Exception:
            print("An error occured")

        df = pd.DataFrame(rows, columns=headers)

        return df.to_csv(index=False, header=True), 200  # return info and 200 OK code


class IntrinsicValue(Resource):
    """ Calculate the intrinsic value of a single stock using Graham's formula. """
    def get(self):

        parser = reqparse.RequestParser()

        parser.add_argument(
            "ticker", type=str, required=True, help="The ticker symbol of the stock"
        )
        parser.add_argument(
            "avg_yield",
            type=float,
            required=True,
            help="Average yield of AAA Corporate Bonds",
        )
        parser.add_argument(
            "cur_yield",
            type=float,
            required=True,
            help="Current yield of AAA Corporate Bonds",
        )

        args = parser.parse_args()

        symbol: str = args.get("ticker")
        avg_yield: float = args.get("avg_yield")
        cur_yield: float = args.get("cur_yield")

        v: float = stock_valuation(symbol, avg_yield, cur_yield)

        return {"value": v}, 200  # return info and 200 OK code


class IntrinsicValues(Resource):
    """ Calculate the intrinsic value for each of the input tickers """
    def get(self):

        parser = reqparse.RequestParser()

        parser.add_argument(
            "tickers", type=str, action='split', required=True, help="One or more ticker symbols"
        )

        parser.add_argument(
            "avg_yield",
            type=float,
            required=True,
            help="Average yield of AAA Corporate Bonds",
        )

        parser.add_argument(
            "cur_yield",
            type=float,
            required=True,
            help="Current yield of AAA Corporate Bonds",
        )

        args = parser.parse_args()

        symbols: list = args.get("tickers")
        avg_yield: float = args.get("avg_yield")
        cur_yield: float = args.get("cur_yield")

        rows: list = []
        headers: list = [
            "Ticker",
            "Intrinsic Value",
        ]

        for symbol in symbols:

            v: float = stock_valuation(symbol, avg_yield, cur_yield)

            row: list = [symbol, v]

            rows.append(row)

        df = pd.DataFrame(rows, columns=headers)

        return df.to_csv(index=False, header=True), 200  # return info and 200 OK code
