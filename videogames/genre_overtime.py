import pandas as pd
import numpy as np
from matplotlib import rcParams

import matplotlib.cm as cm
from scipy.interpolate import interp1d

import matplotlib.pyplot as plt
plt.style.use('rossidata')




def main():
    ### data munging
    data = pd.read_csv('vgsales.csv', encoding="ISO-8859-1")
    data=data.sort_values(by='Year')
    genres=data['Genre'].unique()
    years=np.arange(1980,2018,1)
    genredf=pd.DataFrame(columns=genres)

    for k,year in enumerate(years):
        yeardata=np.zeros((len(data['Genre'].unique())))
        for j,genre in enumerate(genres):
            yeardata[j]=sum(data[(data['Year']==year) & (data['Genre']==genre)]['Global_Sales'])

        genredf.loc[k] = yeardata/np.sum(yeardata)
    plt.close('all')
    fig,ax=plt.subplots()
    colors = cm.rainbow(np.linspace(0, 1, 12))
    xnew = np.linspace(min(years), max(years), num=201, endpoint=True)
    vals=[]
    for j,genre in enumerate(genres):
        x=years
        y=genredf[genre]
        f2 = interp1d(x, y, kind='slinear')

        vals.append(f2(xnew))
    ax.stackplot(xnew, vals,colors=colors,labels=genres)
    handles, labels = ax.get_legend_handles_labels()

    ax.legend(handles[::-1], labels[::-1],bbox_to_anchor=(1.35, 1),borderaxespad=0.)
    # ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    ax.set_xlim([1979,2016])
    # ax.legend()
    plt.savefig('videogames.pdf',dpi=300)


if __name__ == "__main__":

    main()
