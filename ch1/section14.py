def calculate_pi(n_terms: int) -> float:
    numerator: float = 4.0
    denominator: float = 1.0
    pi_approx: float = 0.0
    sign_next_term: float = 1.0
    step: int = 0
    while step < n_terms:
        pi_approx += sign_next_term*numerator/denominator
        step += 1
        sign_next_term *= -1
        denominator += 2
    return pi_approx


def test_calculate_pi_3():
    pi_answer = 4.0 - (4.0/3.0) + (4.0/5.0)
    assert pi_answer == calculate_pi(3)

if __name__ == "__main__":
    test_calculate_pi_3()