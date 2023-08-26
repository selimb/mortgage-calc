import decimal
from mortgage_calc.__mortgage import Mortgage


class Test_monthly_payment:
    def test_excel_example(self) -> None:
        """
        Numbers from https://support.microsoft.com/en-us/office/pmt-function-0214da64-9a63-4996-bc20-214433fa6441.
        """
        rate_annual = 0.08
        months = 10
        principal = 10_000

        m = Mortgage(rate_annual, months, principal)
        monthly = m.monthly_payment()
        assert monthly == decimal.Decimal("1_037.03")
