#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16/12/11 上午11:06
# @Author  : Qiyuan Li @ CUEB
# @Site    : https://github.com/lqyjasonlee/study
# @File    : FF1993.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt


def set_explanatory_matrix(col_list, data):
    X = data[col_list]
    X = sm.add_constant(X)
    return X


def get_parameters(y, X):
    reg_model = sm.OLS(y, X)
    mod_result = reg_model.fit()
    return mod_result.params


def get_parameters_all(y, X, t=201610):
    index_of_t = list(data['DATE']).index(t)
    total = len(data.index)
    params = pd.DataFrame()
    for i in range(index_of_t, total):
        y_cut = y[0: i]
        X_cut = X[0: i]
        params = pd.concat([params, get_parameters(y_cut, X_cut)], axis=1)
    return params


if __name__ == '__main__':

    # 3 factors
    '''
    returns = pd.read_csv('/Users/apple/Desktop/PythonStudy/Finance/25_Portfolios_5x5.CSV')
    explanatory = pd.read_csv('/Users/apple/Desktop/PythonStudy/Finance/F-F_Research_Data_Factors.CSV')

    data = returns.merge(explanatory, on='DATE')
    #print(data.columns)

    X = set_explanatory_matrix(['Mkt-RF', 'SMB', 'HML'], data)

    parameters = get_parameters_all(data['ME1 BM4'], X, 200302)
    parameters = parameters.T

    date = range(len(parameters['const']))
    for i in range(4):
        p = plt.subplot(2, 2, i + 1)
        plt.plot(date, parameters[parameters.columns[i]])
        plt.xlabel('Date')
        if parameters.columns[i] == 'const':
            plt.ylabel('Intercept')
        else:
            plt.ylabel('Beta of %s' % parameters.columns[i])
    plt.show()
    '''



    # 5 factors

    returns = pd.read_csv('/Users/apple/Desktop/PythonStudy/Finance/32_Portfolios_ME_BEME_OP_2x4x4.CSV')
    explanatory = pd.read_csv('/Users/apple/Desktop/PythonStudy/Finance/F-F_Research_Data_5_Factors_2x3.CSV')

    data = returns.merge(explanatory, on='DATE')
    #print(data.columns)

    X = set_explanatory_matrix(['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA'], data)

    reg_model = sm.OLS(data['SMALL LoBM LoOP'], X)
    mod_result = reg_model.fit()
    print(mod_result.summary())

    parameters = get_parameters_all(data['ME1 BM1 OP3'], X, 200802)
    parameters = parameters.T

    date = range(len(parameters['const']))
    for i in range(6):
        p = plt.subplot(3, 2, i + 1)
        plt.plot(date, parameters[parameters.columns[i]])
        plt.xlabel('Date')
        if parameters.columns[i] == 'const':
            plt.ylabel('Intercept')
        else:
            plt.ylabel('Beta of %s' % parameters.columns[i])
    plt.show()
