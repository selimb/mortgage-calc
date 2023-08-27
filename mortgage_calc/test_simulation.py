from mortgage_calc.simulation import RateOverPeriod, amortize_multi


class Test_simulate:
    def test_trivial(self) -> None:
        mortgage = 300_000
        months_total = 25 * 12
        rate_annual_percent = 5

        schedule1 = amortize_multi(
            mortgage, months_total, [RateOverPeriod(rate_annual_percent, 36)]
        )

        schedule2 = amortize_multi(
            mortgage,
            months_total,
            [RateOverPeriod(rate_annual_percent, 12)] * 3,
        )

        for i in range(months_total):
            try:
                assert schedule1[i].rounded() == schedule2[i].rounded()
            except AssertionError as ex:
                raise AssertionError(f"Failed on {i}\n{ex}") from None
