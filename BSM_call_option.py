#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16/9/22 15:25
# @Author  : Jason Li @ CUEB
# @Site    : https://github.com/lqyjasonlee/study
# @File    : BSM_call_option.py
# @Software: PyCharm

from scipy import stats
from math import log, sqrt, exp

class call_option:
    def __init__(self, S0, K, T, t, r, sigma):
        self.S0 = float(S0)
        self.K = K
        self.T = T
        self.t = t
        self.r = r
        self.sigma = sigma
        self.d1 = (log(S0 / K) + (r + 0.5 * sigma ** 2) * (T - t)) / (sigma * sqrt(T - t))
        self.d2 = (log(S0 / K) + (r - 0.5 * sigma ** 2) * (T - t)) / (sigma * sqrt(T - t))

    def val(self):
        val = self.S0 * stats.norm.cdf(self.d1) - self.K * exp(- self.r * (self.T - self.t)) \
                * stats.norm.cdf(self.d2)
        return val

    def delta(self):
        delta = stats.norm.cdf(self.d1)
        return delta

    def gamma(self):
        gamma = stats.norm.pdf(self.d1) / (self.S0 * self.sigma * sqrt(self.T - self.t))
        return gamma

    def theta(self, gamma):
        theta = - self.r * self.K * (sqrt(self.T - self.t)) * stats.norm.cdf(self.d2) - 0.5 * gamma \
                * (self.S0 * self.sigma) * (self.S0 * self.sigma)
        return theta

    def kappa(self):
        kappa = (stats.norm.cdf(- self.d2) - 1.00) * exp(- self.r * (self.T - self.t))
        return kappa

    def rho(self):
        rho = self.K * (self.T - self.t) * stats.norm.cdf(self.d2) * exp( - self.r * (self.T - self.t))
        return rho

    def vega(self):
        vega = self.K * stats.norm.cdf(self.d1) * sqrt(self.T - self.t)
        return vega

    def impvol(self, C0, sigma_est=0.2, N=1000):
        opts = call_option(self.S0, self.K, self.T, self.t, self.r, sigma_est)
        for i in range(N):
            opts.sigma = opts.sigma - (opts.val() - C0) / opts.vega()
        return opts.sigma

    def prt_option_info(self):
        call_price = call_option(self.S0, self.K, self.T, self.t, self.r, self.sigma)
        value = call_price.val()
        veg = call_price.vega()
        delt = call_price.delta()
        gam = call_price.gamma()
        thet = call_price.theta(gam)
        kapp = call_price.kappa()
        rh = call_price.rho()
        iv = call_price.impvol(C0=value)
        print('When we assume \nS0=%f K=%f r=%f sigma=%f' % (self.S0, self.K, self.r, self.sigma))
        print('The length T\t=%f and the start time t\t=%f' % (self.T, self.t))
        print('The price of call option \t=\t%f' % value)
        print('===============The Greek info===============')
        print('The Delta of call option \t=\t %f' % delt)
        print('The Gamma of call option \t=\t %f' % gam)
        print('The Theta of call option \t=\t %f' % thet)
        print('The Kappa of call option \t=\t %f' % kapp)
        print('The Rho of call option \t\t=\t %f' % rh)
        print('The Vega of call option \t=\t %f' % veg)
        print('The implied volatility \t\t=\t %f' % iv)
        return None
