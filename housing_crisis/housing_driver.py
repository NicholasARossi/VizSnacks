
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('rossidata')

def main():
    ### Importing all data

    titles = ['Table 9 89 means', 'Table 9 92 means', 'Table 9 95 means', 'Table 9 98 means', 'Table 9 01 means',
              'Table 9 04 means', 'Table 9 07 means', 'Table 9 10 means', 'Table 9 13 means', 'Table 9 16 means']

    list = []
    xls = pd.ExcelFile('data.xlsx')
    for title in titles:
        df1 = pd.read_excel(xls, title)

        df1.columns = ['class', 'Vehicles', 'Primary residence', 'Other residential property',
                       'Equity in nonresidential property', 'Business equity', 'Other', 'Any nonfinancial asset',
                       'any asset']
        # df2 = pd.read_excel(xls, 'Sheet2')
        df1 = df1.dropna()
        df1 = df1.set_index('class')
        list.append(df1)
    titles = ['Table 9 89', 'Table 9 92', 'Table 9 95', 'Table 9 98', 'Table 9 01', 'Table 9 04', 'Table 9 07',
              'Table 9 10', 'Table 9 13', 'Table 9 16']
    list_median = []
    for title in titles:
        df1 = pd.read_excel(xls, title)

        df1.columns = ['class', 'Vehicles', 'Primary residence', 'Other residential property',
                       'Equity in nonresidential property', 'Business equity', 'Other', 'Any nonfinancial asset',
                       'any asset']
        # df2 = pd.read_excel(xls, 'Sheet2')
        df1 = df1.dropna()
        df1 = df1.set_index('class')
        list_median.append(df1)

    titles = ['Table 6 89 means', 'Table 6 92 means', 'Table 6 95 means', 'Table 6 98 means', 'Table 6 01 means',
              'Table 6 04 means', 'Table 6 07 means', 'Table 6 10 means', 'Table 6 13 means', 'Table 6 16 means']
    capital_means = []
    for title in titles:
        df1 = pd.read_excel(xls, title)
        df1.columns = ['Family characteristic', 'Transaction accounts', 'Certificates of deposit',
                       'Savings bonds',
                       'Bonds',
                       'Stocks',
                       'Pooled investment funds',
                       'Retirement  accounts',
                       'Cash value life insurance',
                       'Other managed assets',
                       'Other ',
                       'Any financial asset']

        df1 = df1.drop(df1.index[[0]])
        df1 = df1.dropna()
        df1 = df1.set_index('Family characteristic')
        capital_means.append(df1)

    titles = ['Table 6 89', 'Table 6 92', 'Table 6 95', 'Table 6 98', 'Table 6 01', 'Table 6 04', 'Table 6 07',
              'Table 6 10', 'Table 6 13', 'Table 6 16']
    capital_medians = []
    for title in titles:
        df1 = pd.read_excel(xls, title)
        df1.columns = ['Family characteristic', 'Transaction accounts', 'Certificates of deposit',
                       'Savings bonds',
                       'Bonds',
                       'Stocks',
                       'Pooled investment funds',
                       'Retirement  accounts',
                       'Cash value life insurance',
                       'Other managed assets',
                       'Other ',
                       'Any financial asset']
        df1 = df1.drop(df1.index[[0]])
        df1 = df1.dropna()
        df1 = df1.set_index('Family characteristic')
        capital_medians.append(df1)


    ### Calculating inflation

    inflation = pd.read_csv('cpi.csv')
    infvals = inflation.iloc[0::12][-26:-1][0::3].Index.values
    infvals = np.append(infvals, 236.525)
    infrates = infvals / 236.525

    ### plotting value of primary resisdence value over time

    plt.close('all')
    years = [1989, 1992, 1995, 1998, 2001, 2004, 2007, 2010, 2013, 2016]

    low = []
    for item in list_median:
        low.append(item.loc['Less than 20'].iloc[1]['Primary residence'])

    high = []
    for item in list_median:
        high.append(item.loc['90–100'].iloc[2]['Primary residence'])

    financelow = []
    for item in capital_medians:
        financelow.append(item.loc['Less than 20'].iloc[1]['Any financial asset'])

    financehigh = []
    for item in capital_medians:
        financehigh.append(item.loc['90–100'].iloc[2]['Any financial asset'])
    colors = ['teal', '#e684ae']
    plt.close('all')
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(8, 3))

    # If you'd like to plot the financial values of things replace low with financelow and high with financehigh
    ax.plot(years, low / infrates, color=colors[0], label='poor', marker='o')
    ax.legend()

    ax2.plot(years, high / infrates, color=colors[1], label='rich', marker='o')
    ax2.legend()
    ax.fill_between(np.linspace(2007, 2009, 10), 60, 120, facecolor='grey', alpha=0.25)

    ax2.fill_between(np.linspace(2007, 2009, 10), 250, 600, facecolor='grey', alpha=0.25)
    ax.set_ylabel('Median Weath (thousands)')
    ax.set_xlabel('Year')
    ax2.set_ylabel('Median Weath (thousands)')
    ax2.set_xlabel('Year')
    fig.savefig('figures/housing.pdf')


if __name__ == "__main__":

    main()