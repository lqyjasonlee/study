#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/11 上午11:45
# @Author  : Qiyuan Li @ CUEB
# @Site    : https://github.com/lqyjasonlee/study
# @File    : hw2_17S.py
# @Software: PyCharm

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns


class QuotesData:
    def __init__(self, name, quotes, dates, length):
        self.name = name
        self.quotes = np.array(quotes)
        if type(dates[0]) == datetime.datetime:
            self.dates = dates
        else:
            dates_ = []
            for date in dates:
                dates_.append(datetime.datetime.strptime(date, '%Y-%m-%d'))
            self.dates = dates_
        tdelta = self.dates[0] - self.dates[1]
        if tdelta.days == 1:
            self.data_freq = 'Daily'
        elif tdelta.days >= 28 & tdelta.days <= 32:
            self.data_freq = 'Monthly'
        self.length = length

    def __del__(self):
        class_name = self.__class__.__name__
        print(class_name, ':delete the quotes_data obj')

    def calculate_cc_return(self):
        pt = self.quotes[: -1]
        pt_1 = self.quotes[1:]
        cc_return = np.log(pt / pt_1)
        cc_dates = self.dates[: -1]
        cc_length = self.length - 1
        return QuotesData('cc_return', cc_return, cc_dates, cc_length)

    def plot_quotes_date(self):
        sns.set(color_codes=True)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        if self.data_freq == 'Daily':
            line_width = 0.4
        else:
            line_width = 1
        ax.plot(self.dates, self.quotes, label=self.name, linewidth=line_width)
        ax.set_xlabel('dates')
        ax.set_ylabel(self.name)
        ax.legend(loc='upper left')
        plt.show()
        return None

    def plot_quotes_hist(self):
        sns.set(color_codes=True)
        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        ax1.set_xlabel(self.name)
        ax1.set_ylabel('frequency')
        sns.distplot(cc_return.quotes, ax=ax1, bins=75, kde=True, rug=False, hist=True)
        ax2 = fig.add_subplot(212)
        ax2.set_xlabel(self.name)
        ax2.set_ylabel('frequency')
        sns.kdeplot(cc_return.quotes, ax=ax2, shade=True)
        plt.show()
        return None

    def plot_quotes_qqplot(self):
        from statsmodels.graphics.api import qqplot
        sns.set(color_codes=True)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        qqplot(self.quotes, line='q', ax=ax, fit=True)
        ax.set_xlabel('theoretical quantiles')
        ax.set_ylabel('sample quantiles')
        plt.show()
        return None

    def calculate_quotes_stat(self):
        quotes = pd.DataFrame(self.quotes)
        return quotes.mean(), quotes.var(), quotes.skew(), quotes.kurt()

    def daily_to_monthly(self):
        month = []
        quotes = []
        i = 0
        while i < self.length - 1:
            if i == 0:
                quotes_ = 0
            date_i = self.dates[i]
            date_ip1 = self.dates[i + 1]
            if date_i.month == date_ip1.month:
                quotes_ += self.quotes[i]
                i += 1
            else:
                month.append(date_i)
                quotes.append(quotes_)
                quotes_ = 0
                i += 1
                continue
        return QuotesData('cc_return_monthly', quotes, month, len(month))


if __name__ == '__main__':

    '''Get original quotes data'''
    data = pd.read_csv('/Users/apple/Desktop/PythonStudy/Finance/399300.csv', encoding="gb2312")

    '''Data cleaning'''
    #print(data.columns)
    data.drop(data.columns[1: 3], axis=1, inplace=True)
    data.columns = ['dates', 'quotes']
    #print(data.head())

    '''Get cc_return'''
    close_quotes = QuotesData('closing quotes', data['quotes'], data['dates'], len(data['dates']))

    cc_return = close_quotes.calculate_cc_return()
    #print(cc_return.dates[0: 5], '\n', cc_return.quotes[0: 5])

    #cc_return.plot_quotes_date()
    #cc_return.plot_quotes_hist()
    #cc_return.plot_quotes_qqplot()
    #print(cc_return.calculate_quotes_stat())
    #print(cc_return.length)


    '''Daily into monthly'''
    cc_return_monthly = cc_return.daily_to_monthly()
    '''delete the first month 2017-3'''
    cc_return_monthly = QuotesData('cc_return_monthly', cc_return_monthly.quotes[1:], cc_return_monthly.dates[1:], cc_return_monthly.length - 1)
    #print(cc_return_monthly.quotes[0: 5], cc_return_monthly.dates[0: 5], cc_return_monthly.length, cc_return_monthly.data_freq)
    #cc_return_monthly.plot_quotes_date()
    #cc_return_monthly.plot_quotes_hist()
    #cc_return_monthly.plot_quotes_qqplot()
    #print(cc_return_monthly.calculate_quotes_stat())
    #print(cc_return_monthly.length)
