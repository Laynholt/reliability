from math import exp, pi, gamma
from scipy.integrate import trapz, quad
from scipy.special import erf


class Exponential:
    """
    Экспоненциальное распределение Exp(λ)
    """

    def __init__(self, _lambda: float):
        self._lambda = _lambda
        self.m = 1 / _lambda
        self.sigma = 1 / _lambda

    def f(self, time: int) -> float:
        """ Плотность вероятности """
        return self._lambda * exp(-self._lambda * time)

    def p(self, time: int) -> float:
        """Распределение времени безотказной работы"""
        return exp(-self._lambda * time)


class Rayleigh:
    """
    Распределение Рэлея R(λ)
    """

    def __init__(self, _lambda: float):
        self._lambda = _lambda
        self.m = (pi / (4 * _lambda)) ** 0.5
        self.sigma = ((4 - pi) / (4 * _lambda)) ** 0.5

    def f(self, time: int) -> float:
        """ Плотность вероятности """
        return 2 * self._lambda * time * exp(-self._lambda * time * time)

    def p(self, time: int) -> float:
        """Распределение времени безотказной работы"""
        return exp(-self._lambda * time * time)


class Gamma:
    """
    Гамма-распределение Г(α,β)
    """

    def __init__(self, alpha: int, beta: int):
        self.alpha = alpha
        self.beta = beta
        self.m = alpha * beta
        self.sigma = (alpha * beta) ** 0.5

    def f(self, time: int) -> float:
        """ Плотность вероятности """
        return time ** (self.alpha - 1) * exp(-time / self.beta) / (self.beta ** self.alpha * gamma(self.alpha))

    def p(self, time: int) -> float:
        """Распределение времени безотказной работы"""
        integral, error = quad(lambda x: (x ** (self.alpha - 1)) * exp(-x), 0, time / self.beta)
        return 1 - (1 / gamma(self.alpha)) * integral


class TruncatedNormal:
    """
    Усеченное нормальное распределение TN(m0, ϭ0)
    """

    def __init__(self, m0: int, sigma0: int):
        self.m0 = m0
        self.sigma0 = sigma0
        # self.phi = lambda x: erf(x/2 ** 0.5) / 2

        self.integral, error = quad(lambda x: exp(-x*x / 2), 0, m0 / sigma0)
        self.phi = lambda x: (1 / (2 * pi) ** 0.5) * self.integral

        self.c = 1 / (0.5 + self.phi(m0 / sigma0))
        self.k = self.c / ((2 * pi) ** 0.5) * exp(-m0 * m0 / (2 * sigma0 * sigma0))
        self.m = m0 + self.k * sigma0
        self.sigma = sigma0 * (1 + self.k * m0 / sigma0 - self.k * self.k) ** 0.5

    def f(self, time: int) -> float:
        """ Плотность вероятности """
        return self.c / (self.sigma0 * (2 * pi) ** 0.5) * exp(-(time - self.m0) ** 2 / (2 * self.sigma0 ** 2))

    def p(self, time: int) -> float:
        """Распределение времени безотказной работы"""
        integral, error = quad(lambda x: exp(-x * x / 2), 0, (time - self.m0) / self.sigma0)
        phi = (1 / (2 * pi) ** 0.5) * integral
        # print("time= ", time, " x=", (time - self.m0) / self.sigma0, " phi=", phi)
        return self.c * (0.5 - (phi if phi <= 0.5 else 0.5))


class Weibula:
    """
        Распределение Вейбула W(alpha, beta)
    """

    def __init__(self, alpha: int, beta: int):
        self.alpha = alpha
        self.beta = beta
        self.m = beta * gamma(1 + 1 / alpha)
        self.sigma = beta * (gamma(1 + 2 / alpha) - (gamma(1 + 1 / alpha)) ** 2) ** 0.5

    def f(self, time: int) -> float:
        """ Плотность вероятности """
        return self.alpha * time ** (self.alpha - 1) * exp(-(time / self.beta) ** self.alpha) / self.beta ** self.alpha

    def p(self, time: int) -> float:
        """Распределение времени безотказной работы"""
        return exp(-(time / self.beta) ** self.alpha)
