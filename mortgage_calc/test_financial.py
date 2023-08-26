import doctest
from . import financial
from .financial import IPMT, PMT, AmortizeItem, amortize, rate_calc


def test_doctest() -> None:
    results = doctest.testmod(financial, optionflags=doctest.ELLIPSIS)
    assert results.failed == 0


class Test_PMT:
    def test_example_excel(self) -> None:
        """
        Numbers from https://support.microsoft.com/en-us/office/pmt-function-0214da64-9a63-4996-bc20-214433fa6441.
        """
        rate_annual = 8 / 100
        payments_count = 10
        principal = 10_000

        result = PMT(rate=rate_annual / 12, payments_count=payments_count, principal=principal)
        assert round(result, 2) == 1_037.03


class Test_IPMT:
    def test_example_excel(self) -> None:
        """
        Numbers from https://support.microsoft.com/en-au/office/ipmt-function-5cce0ad6-8402-4a41-8d29-61a0b054cb6f
        """
        rate_annual = 10 / 100
        period = 1
        years = 3
        loan = 8_000

        result = IPMT(rate_annual / 12, period, years * 12, loan)
        assert round(result, 2) == 66.67

        result = IPMT(rate_annual, 3, years, loan)
        assert round(result, 2) == 292.45


class Test_rate_calc:
    def test_example_contextures(self) -> None:
        """
        Numbers from https://www.contextures.com/excelpmtfunction.html, example 2
        """
        rate_annual = 5 / 100
        principal = 100_000
        months = 240
        rate_monthly = rate_calc(rate_annual)
        result = PMT(rate_monthly, months, principal)

        assert round(result, 2) == 657.13


class Test_amortize:
    def test_example_centris(self) -> None:
        """
        From https://www.centris.ca/en/tools/calculator
        """
        mortgage = 300_000
        rate_annual = 5.00 / 100
        rate_monthly = rate_calc(rate_annual)
        months = 25 * 12

        schedule = amortize(mortgage, rate_monthly, months)

        print(
            "\n".join(
                [
                    f"{i.payment_number} {i.principal} {i.interest} {i.balance}"
                    for i in (i.rounded() for i in schedule)
                ]
            )
        )

        first = schedule[0]
        assert first.rounded() == AmortizeItem(
            payment_number=1,
            payment=1_744.81,
            principal=508,
            interest=1237,
            principal_total=508,
            interest_total=1237,
            balance=299_492,
        )

        second = schedule[1]
        assert second.rounded() == AmortizeItem(
            payment_number=2,
            payment=1_744.81,
            principal=510,
            interest=1235,
            principal_total=round(first.principal + second.principal),
            interest_total=round(first.interest + second.interest),
            balance=298983,
        )

        assert len(schedule) == months

        last = schedule[-1].rounded()
        assert f"{last.principal_total} {last.balance} {last.interest_total}" == "300000 0 223444"
