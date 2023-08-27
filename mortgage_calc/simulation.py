from typing import NamedTuple

from mortgage_calc.financial import AmortizeItem, RateCalcCompound, amortize, rate_calc


class RateOverPeriod(NamedTuple):
    rate_annual_percent: float
    """Annual interest rate, as a *percentage*."""
    months: int


def amortize_multi(
    loan_amount: float,
    loan_term: int,
    rates: list[RateOverPeriod],
    *,
    extrapolate: bool = True,
    compound: RateCalcCompound = "semi-annual",
) -> list[AmortizeItem]:
    """
    Computes the amortization schedule for a loan at varying rates.

    :param loan_amount: Loan amount.
    :param loan_term: Loan term.
    :param rates: List of rates and periods.
    :param extrapolate: Whether to "extrapolate" the amortization schedule over
        the entire loan term if the remaining balance is greater than zero.
        The last rate in `rates` is used in that case.
    """
    ret: list[AmortizeItem] = []

    balance = loan_amount
    months_left = loan_term
    last: AmortizeItem | None = None

    for rate_annual_percent, months in rates:
        term_schedule = amortize(
            balance,
            months_left,
            rate_calc(rate_annual_percent / 100, compound),
            last=last,
        )[:months]
        ret += term_schedule
        last = term_schedule[-1]
        balance = last.balance
        months_left = loan_term - last.payment_number

    if balance > 0 and extrapolate:
        term_schedule = amortize(
            balance,
            months_left,
            rate_calc(rates[-1].rate_annual_percent / 100, compound),
            last=last,
        )
        ret += term_schedule

    return ret
