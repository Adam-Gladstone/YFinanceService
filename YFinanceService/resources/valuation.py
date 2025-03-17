"""
Estimates the intrinsic value of a stock
"""


def stock_valuation_graham(
    eps: float, pe_base: float, g: float, avg_yield: float, cur_yield: float
) -> float:
    """
    Calculate the intrinsic value of a stock using Graham's formula
    Reference: https://stablebread.com/how-to-calculate-the-intrinsic-value-of-a-company-like-benjamin-graham/

        V = (eps * (pe_base + 2g) * avg_yield) / cur_yield

    where:
    V = intrinsic value per share (over the next 7-10 years)
        EPS = earnings per share (over the trailing twelve months (TTM))
        8.5 = price-to-earnings (P/E) base for a no-growth company
        g = reasonably expected annual growth rate (over the next 7-10 years)
        avg_yield = average yield of AAA Corporate Bonds
        cur_yield = current yield of AAA Corporate Bonds
    """

    V = (eps * (pe_base + 1.1 * g) * avg_yield) / cur_yield

    return V
