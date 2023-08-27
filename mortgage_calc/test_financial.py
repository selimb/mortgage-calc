import doctest
from . import financial
from .financial import PMT, AmortizeItem, amortize, rate_calc


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

        print(fmt_schedule(schedule))

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

    def test_multi_trivial(self) -> None:
        """
        It's hard to get accurate examples, so this instead tests a trivial case: 2-year schedule
        two 1-year schedule, using the same rate.
        """
        mortgage = 300_000
        months_total = 25 * 12
        rate_monthly = rate_calc(5 / 100)

        # 2 years fixed
        schedule1 = amortize(mortgage, months_total, rate_monthly)[: 2 * 12]

        # 2 * (1 year fixed), same rate
        schedule2_1 = amortize(mortgage, months_total, rate_monthly)[: 1 * 12]
        last = schedule2_1[-1]
        assert last.payment_number == 12
        schedule2_2 = amortize(
            mortgage - last.principal_total,
            months_total - last.payment_number,
            rate_monthly,
            last=last,
        )[: 1 * 12]

        # Debugging
        # print("schedule1\n" + fmt_schedule(schedule1))
        # print("schedule2_1\n" + fmt_schedule(schedule2_1))
        # print("schedule2_2\n" + fmt_schedule(schedule2_2))

        assert schedule1[-1] == schedule2_2[-1]


def fmt_schedule(schedule: list[AmortizeItem]) -> str:
    return "\n".join(
        [
            f"{i.payment_number} {i.payment} {i.principal} {i.interest} {i.balance}"
            for i in (i.rounded() for i in schedule)
        ]
    )
