#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/12 上午7:00
# @Author  : Qiyuan Li @ CUEB
# @Site    : https://github.com/lqyjasonlee/study
# @File    : hw4_17S.py
# @Software: PyCharm

import numpy as np
import pandas as pd
import statsmodels.tsa.arima_model as smt
import statsmodels.api as sm

if __name__ == '__main__':
    #question2
    '''
    data = pd.read_csv('/Users/apple/Desktop/PythonStudy/Finance/hw4q2.csv', header=None)
    y = np.array(data[0])
    model = smt.ARMA(y, (1, 1))
    result = model.fit(method='mle') #method='css' if use conditional MLE
    print(result.summary())
    '''
    #question3
    rho_0 = 1 #or rho_0 = 0.5
    rho_cap = []
    t_cap = []
    for i in range(1000):
        y = []
        y0 = 0
        epsilon = np.random.normal(0, 1, 1000)
        y.append(epsilon[0])
        for j in range(999):
            y.append(rho_0 * y[j] + epsilon[j + 1])
        y = np.array(y)
        model = sm.OLS(y[1:999], y[0:998])
        result = model.fit()
        rho = result.params[0]
        std = rho / result.tvalues[0]
        t = (rho - rho_0) / std
        rho_cap.append(rho)
        t_cap.append(t)
    rho_cap = np.array(rho_cap)
    t_cap = np.array(t_cap)
    print(np.percentile(t_cap, 95), np.percentile(t_cap, 97.5))