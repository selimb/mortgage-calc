def PMT(*, rate: float, payments_count: int, principal: float) -> float:
    """
    Like PMT from excel.

    :param rate: Interest rate for the loan.
    :param payments_count: Total number of payments.
    :param principal: Loan amount.
    """
    # https://en.wikipedia.org/wiki/Mortgage_calculator#Monthly_payment_formula
    r = rate
    N = payments_count
    P = principal

    return (r * P) / (1 - (1 + r) ** (-N))
