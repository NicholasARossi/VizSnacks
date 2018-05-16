import pandas as pd
import numpy as np
from matplotlib import animation, rc
import matplotlib.pyplot as plt
#plt.style.use('rossidata')




def main():
    ### data munging
    data = pd.read_csv('irm.csv', encoding="ISO-8859-1")
    #calculate how different the rate of interracial marriage is compared to the popluation
    data['normalized']=data['IRM_rate']/(1-data['percentage_pop'])
    dataS = data.sort_values(by=['normalized'])

    ### plotting
    plt.close('all')
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.barh(dataS['class'], dataS['normalized'])
    vals = ax.get_xticks()

    ax.set_xticklabels(['{:3.0f}%'.format(x * 100) for x in vals])
    ax.set_xlabel('Percentage of Interracial Marriage as Fraction of Random Marriages')
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    fig.savefig('bar.png', dpi=300)

if __name__ == "__main__":

    main()
