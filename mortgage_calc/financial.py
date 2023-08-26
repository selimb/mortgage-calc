from typing import Literal


def PMT(rate: float, payments_count: int, principal: float) -> float:
    """
    Like PMT from excel.

    :param rate: Interest rate for the loan.
    :param payments_count: Total number of payments.
    :param principal: Loan amount.
    """
    # https://en.wikipedia.org/wiki/Mortgage_calculator#Monthly_payment_formula
    r = rate
    N = payments_count
    P = principal

    return (r * P) / (1 - (1 + r) ** (-N))


def rate_calc(rate_annual: float, compound: Literal["semi-annual"] = "semi-annual") -> float:
    """
    Calculates monthly interest rate for different compounding methods.

    >>> rate = 5/100
    >>> (rate / 12)*100
    0.41666...
    >>> rate_calc(rate, "semi-annual")*100
    0.41239...
    """
    r = rate_annual
    match compound:
        case "semi-annual":
            # From https://www.contextures.com/excelpmtfunction.html, example 2
            # In Canada, mortgage interest rates are compounded semi-annually, by law.
            # https://www.nesto.ca/featured-articles/mortgage-principal-and-interest-explained/
            return (r / 2 + 1) ** (1 / 6) - 1
