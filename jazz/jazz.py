import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('rossidata')
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def main():
    text_file = open(r"data.txt", "r", encoding="utf-8")
    text_file=list(text_file)

    text_file2 = open(r"dates.txt", "r", encoding="utf-8")
    text_file2=list(text_file2)
    expectancies=[float(x.split('\n')[0]) for x in text_file2[2::6]]
    names=[]
    birth=[]
    death=[]

    for text in text_file:
        names.append(text.replace(']]','[[').split('[[')[1])
        birth.append(text.replace('-','–').replace('(','–').split('–')[1])
        death.append(text.replace('-','–').replace(')','–').split('–')[1])

    indexors=np.array([len(x)<5 for x in birth]).ravel()
    names=np.asarray(names)[indexors]
    birth=np.asarray(birth)[indexors]
    death=np.asarray(death)[indexors]
    d = {'names': names, 'birth': birth, 'death': death}
    df = pd.DataFrame(data=d)
    df['birth']=df['birth'].apply(int)
    df['death']=df['death'].apply(int)
    df['lives']=df['death']-df['birth']

    differences=[]
    expected=[]
    years=np.arange(1900,1999)
    for x in range(len(df)):
        differences.append(df['lives'].iloc[x]-expectancies[find_nearest(years,df['birth'].iloc[x])])
        expected.append(expectancies[find_nearest(years,df['birth'].iloc[x])])

    df['differences']=differences
    df['expected']=expected
    sorted_values=df.sort_values(by='differences')
    edited=pd.concat([sorted_values['names'],sorted_values['lives'],sorted_values['differences']], axis=1)
    edited['differences']=abs(edited['differences'])
    edited=edited.set_index('names')
    plt.close('all')
    fig,ax=plt.subplots()
    edited.iloc[0:15].plot(kind='bar',stacked='true',ax=ax)

    fig.savefig('jazzbar.pdf')

if __name__ == "__main__":

    main()
