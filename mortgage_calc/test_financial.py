import doctest
from . import financial
from .financial import PMT, rate_calc


def test_doctest() -> None:
    results = doctest.testmod(financial, optionflags=doctest.ELLIPSIS)
    assert results.failed == 0


class Test_PMT:
    def test_excel_example(self) -> None:
        """
        Numbers from https://support.microsoft.com/en-us/office/pmt-function-0214da64-9a63-4996-bc20-214433fa6441.
        """
        rate_annual = 0.08
        payments_count = 10
        principal = 10_000

        result = PMT(rate=rate_annual / 12, payments_count=payments_count, principal=principal)
        assert round(result, 2) == 1_037.03


class Test_rate_calc:
    def test_contextures_example(self) -> None:
        """
        Numbers from https://www.contextures.com/excelpmtfunction.html, example 2
        """
        rate_annual = 5 / 100
        principal = 100_000
        months = 240
        rate_monthly = rate_calc(rate_annual)
        result = PMT(rate_monthly, months, principal)

        assert round(result, 2) == 657.13

    def test_td_bank_example(self) -> None:
        """
        From https://apps.td.com/mortgage-payment-calculator/, with:
        - mortgage = 300_000
        - 3 year fixed rate @ 6.71%
        - 25 years
        - monthly payments
        """
