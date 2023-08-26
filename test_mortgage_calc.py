from mortgage_calc import PMT


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
