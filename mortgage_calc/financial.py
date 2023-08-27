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


RateCalcCompound = Literal["semi-annual", "month"]


def rate_calc(rate_annual: float, compound: RateCalcCompound = "semi-annual") -> float:
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
    loan_term: int,
    rate_monthly: float,
    *,
    last: AmortizeItem | None = None,
) -> list[AmortizeItem]:
    """
    Computes the amortization schedule for a loan at a single fixed rate.

    :param loan_amount: Loan amount.
    :param rate_monthly: Monthly interest rate, as calculated by `rate_calc`.
    :param loan_term: Total length of the loan in months. Usually 300 (25 years).
    :param last: Last amortization item. See below.

    To compute an amortization schedule with varying interest rates, use the following:

        mortgage = 300_000
        loan_term = 25*12
        # 3 years @ 5%
        rate1 = rate_calc(0.05)
        rate1_period = 3*12
        # 2 years @ 4%
        rate2 = rate_calc(0.04)
        rate2_period = 2*12

        schedule1 = amortize(
            mortgage,
            loan_term
            rate1,
        )[: rate1_period]

        schedule2 = amortize(
            mortgage - schedule[-1].principal_total,
            loan_term - rate2_period,
            rate2,
            last=schedule[-1],
        )[: rate2_period]

    You can also re-finance
    """
    number = 1 if last is None else last.payment_number + 1
    principal_total = 0 if last is None else last.principal_total
    interest_total = 0 if last is None else last.interest_total
    payment = PMT(rate_monthly, loan_term, loan_amount)
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
