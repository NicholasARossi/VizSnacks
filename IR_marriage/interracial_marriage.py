import pandas as pd
import numpy as np
from matplotlib import animation, rc
import matplotlib.pyplot as plt
plt.style.use('rossidata')




def main():
    ### data munging
    data = pd.read_csv('irm.csv', encoding="ISO-8859-1")
    #calculate how different the rate of interracial marriage is compared to the popluation
    data['normalized']=data['IRM_rate']/(1-data['percentage_pop'])
    dataS = data.sort_values(by=['normalized'])

    ### plotting
    plt.close('all')
    fig, (ax, ax0) = plt.subplots(2, 1, figsize=(6, 12), sharey=True)

    ax.bar(data['class'][1::2], data['normalized'][1::2])
    vals = ax.get_yticks()

    ax.set_yticklabels(['{:3.0f}%'.format(x * 100) for x in vals])
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    # fig.savefig('bar.png',dpi=300)


    ax0.bar(data['class'][::2], data['normalized'][::2], color="#FF8888")
    vals = ax0.get_yticks()

    ax0.set_yticklabels(['{:3.0f}%'.format(x * 100) for x in vals])
    ax0.spines['left'].set_visible(False)
    ax0.spines['bottom'].set_visible(False)
    fig.savefig('bar.png')


if __name__ == "__main__":

    main()
