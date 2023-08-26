#
# Copied from https://github.com/jbmohler/mortgage
#
from __future__ import print_function
import decimal

MONTHS_IN_YEAR = 12
DOLLAR_QUANTIZE = decimal.Decimal(".01")


def dollar(f: float | decimal.Decimal, round: str = decimal.ROUND_CEILING) -> decimal.Decimal:
    """
    This function rounds the passed float to 2 decimal places.
    """
    if not isinstance(f, decimal.Decimal):
        f = decimal.Decimal(str(f))
    return f.quantize(DOLLAR_QUANTIZE, rounding=round)


class Mortgage:
    def __init__(self, interest: float, months: int, amount: float) -> None:
        self._interest = float(interest)
        self._months = int(months)
        self._amount = dollar(amount)

    def rate(self):
        return self._interest

    def month_growth(self):
        return 1.0 + self._interest / MONTHS_IN_YEAR

    def apy(self):
        return self.month_growth() ** MONTHS_IN_YEAR - 1

    def loan_years(self):
        return float(self._months) / MONTHS_IN_YEAR

    def loan_months(self):
        return self._months

    def amount(self):
        return self._amount

    def monthly_payment(self):
        pre_amt = (
            float(self.amount())
            * self.rate()
            / (float(MONTHS_IN_YEAR) * (1.0 - (1.0 / self.month_growth()) ** self.loan_months()))
        )
        return dollar(pre_amt, round=decimal.ROUND_CEILING)

    # def total_value(self, m_payment):
    #     return (
    #         m_payment
    #         / self.rate()
    #         * (float(MONTHS_IN_YEAR) * (1.0 - (1.0 / self.month_growth()) ** self.loan_months()))
    #     )

    def annual_payment(self):
        return self.monthly_payment() * MONTHS_IN_YEAR

    def total_payout(self):
        return self.monthly_payment() * self.loan_months()

    def monthly_payment_schedule(self):
        monthly = self.monthly_payment()
        balance = dollar(self.amount())
        rate = decimal.Decimal(str(self.rate())).quantize(decimal.Decimal(".000001"))
        while True:
            interest_unrounded = balance * rate * decimal.Decimal(1) / MONTHS_IN_YEAR
            interest = dollar(interest_unrounded, round=decimal.ROUND_HALF_UP)
            if monthly >= balance + interest:
                yield balance, interest
                break
            principle = monthly - interest
            yield principle, interest
            balance -= principle


def print_summary(m: Mortgage):
    print("{0:>25s}:  {1:>12.6f}".format("Rate", m.rate()))
    print("{0:>25s}:  {1:>12.6f}".format("Month Growth", m.month_growth()))
    print("{0:>25s}:  {1:>12.6f}".format("APY", m.apy()))
    print("{0:>25s}:  {1:>12.0f}".format("Payoff Years", m.loan_years()))
    print("{0:>25s}:  {1:>12.0f}".format("Payoff Months", m.loan_months()))
    print("{0:>25s}:  {1:>12.2f}".format("Amount", m.amount()))
    print("{0:>25s}:  {1:>12.2f}".format("Monthly Payment", m.monthly_payment()))
    print("{0:>25s}:  {1:>12.2f}".format("Annual Payment", m.annual_payment()))
    print("{0:>25s}:  {1:>12.2f}".format("Total Payout", m.total_payout()))
