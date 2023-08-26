from typing import NamedTuple

from mortgage_calc.financial import AmortizeItem, amortize, rate_calc


class RateOverPeriod(NamedTuple):
    rate_annual: float
    months: int


def simulate(mortgage: float, months_total: int, rates: list[RateOverPeriod]) -> list[AmortizeItem]:
    ret: list[AmortizeItem] = []

    balance = mortgage
    months_left = months_total
    last: AmortizeItem | None = None

    for rate_annual, months in rates:
        term_schedule = amortize(
            balance,
            rate_calc(rate_annual),
            months_left,
            last=last,
        )[:months]
        ret += term_schedule
        last = term_schedule[-1]
        balance = last.balance
        months_left = months_total - last.payment_number

    if balance > 0:
        print(balance, rates[-1].rate_annual, months_left)
        term_schedule = amortize(
            balance,
            rate_calc(rates[-1].rate_annual),
            months_left,
            last=last,
        )
        ret += term_schedule

    return ret
