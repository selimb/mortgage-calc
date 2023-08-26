from mortgage_calc.simulation import RateOverPeriod, simulate


class Test_simulate:
    def test_simple(self) -> None:
        # Like Test_amortize.test_using_last_simple
        mortgage = 300_000
        months_total = 25 * 12
        rate_annual = 5 / 100

        schedule1 = simulate(mortgage, months_total, [RateOverPeriod(rate_annual, 36)])

        schedule2 = simulate(
            mortgage,
            months_total,
            [RateOverPeriod(rate_annual, 12)] * 3,
        )

        for i in range(months_total):
            try:
                assert schedule1[i].rounded() == schedule2[i].rounded()
            except AssertionError as ex:
                raise AssertionError(f"Failed on {i}\n{ex}") from None
