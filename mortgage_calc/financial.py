from __future__ import annotations
import dataclasses
from typing import Literal
from typing_extensions import assert_never


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


def rate_calc(
    rate_annual: float, compound: Literal["semi-annual", "month"] = "semi-annual"
) -> float:
    """
    Calculates monthly interest rate for different compounding methods.

    >>> rate = 5/100
    >>> (rate / 12)*100
    0.41666...
    >>> rate_calc(rate, "month")*100
    0.41666...
    >>> rate_calc(rate, "semi-annual")*100
    0.41239...
    """
    r = rate_annual
    if compound == "semi-annual":
        periods = 2
    elif compound == "month":
        periods = 12
    else:
        assert_never(compound)
    months_per_period = 12 / periods
    # From https://www.contextures.com/excelpmtfunction.html, example 2
    # In Canada, mortgage interest rates are compounded semi-annually, by law.
    # https://www.nesto.ca/featured-articles/mortgage-principal-and-interest-explained/
    return (r / periods + 1) ** (1 / months_per_period) - 1


@dataclasses.dataclass
class AmortizeItem:
    payment_number: int
    payment: float
    principal: float
    interest: float
    principal_total: float
    interest_total: float
    balance: float

    def rounded(self) -> AmortizeItem:
        return AmortizeItem(
            payment_number=self.payment_number,
            payment=self.payment,
            principal=round(self.principal),
            interest=round(self.interest),
            principal_total=round(self.principal_total),
            interest_total=round(self.interest_total),
            balance=round(self.balance),
        )


MONTHS_PER_YEAR = 12


def amortize(
    loan_amount: float,
    rate_monthly: float,
    payments_count: int,
    *,
    last: AmortizeItem | None = None,
) -> list[AmortizeItem]:
    number = 1 if last is None else last.payment_number + 1
    principal_total = 0 if last is None else last.principal_total
    interest_total = 0 if last is None else last.interest_total
    payment = PMT(rate_monthly, payments_count, loan_amount)
    ret: list[AmortizeItem] = []
    balance = loan_amount
    while True:
        # Accumulate values instead of using IPMT, like in https://github.com/jbmohler/mortgage/blob/e4ecef1eeeceebfc51f3421f077727e5abefee17/mortgage.py#L62
        interest = balance * rate_monthly
        interest_total += interest
        principal = payment - interest
        principal_total += principal
        balance -= principal
        ret.append(
            AmortizeItem(
                payment_number=number,
                payment=round(payment, 2),
                principal=round(principal, 2),
                interest=round(interest, 2),
                principal_total=round(principal_total, 2),
                interest_total=round(interest_total, 2),
                balance=round(balance, 2),
            )
        )
        if balance <= 0:
            break
        number += 1
    return ret
