import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('rossidata')
from colour import Color


def main():
    """ This function processes all the data and outputs a javascript object that can be read by the associated .js file"""
    df = pd.read_json('delays.json')
    keys = pd.read_csv('ICAO_airports.csv', error_bad_lines=False, encoding="ISO-8859-1")

    codes = df['icao code'].unique()
    columns = ['code','airport', 'state', 'lat', 'long', 'delay15', 'delay30', 'delay45', 'observations', 'ontime']
    df_ = pd.DataFrame(columns=columns)

    for code in codes:
        slico = df[df['icao code'] == code]
        lat, long = keys[keys['ident'] == code]['latitude_deg'], keys[keys['ident'] == code]['longitude_deg']
        state = list(keys[keys['ident'] == code]['iso_region'])[0].split('-')[1]
        tempair=slico['airport'].iloc[0]
        if 'International' in tempair:
            airport=tempair.split('International')[0]
        else:
            airport=tempair.split('Airport')[0]

        df2 = pd.DataFrame([[code, airport,state, float(lat), float(long), sum(slico['delayed15']), sum(slico['delayed30']),
                             sum(slico['delayed45']), sum(slico['observations']), sum(slico['ontime'])]],
                           columns=columns)
        df_ = df_.append(df2)
    df_['late'] = df_['observations'] - df_['ontime']
    states = {
        'CA': 'California',
        'FL': 'Florida',
        'GA': 'Georgia',
        'IL': 'Illinois',
        'NY': 'New York',
        'TX': 'Texas'
    }

    ### Worst airports bars


    worst_bylate=df_.sort_values(by='late',ascending=[False]).iloc[0:11]


    plt.close('all')
    fig,ax=plt.subplots()
    objects = worst_bylate['late']
    y_pos = np.arange(len(objects))

    ax.bar(y_pos * 1.5 + 1, objects[::-1], align='center', color=["turquoise"])
    ax.set_xticks(y_pos * 1.5 + 1)
    ax.set_xticklabels(worst_bylate['airport'][::-1])
    # ax.set_xlim([0, 45])
    plt.xticks(rotation=-270)

    plt.savefig('worstairports_volume.png',dpi=300)

    plt.close('all')
    fig,ax=plt.subplots()
    objects = (worst_bylate['late']/worst_bylate['observations'])* 100
    y_pos = np.arange(len(objects))

    star = Color("#e7e1ef")
    mid = Color("#c994c7")
    end = Color("#dd1c77")

    colors = list(star.range_to(mid, 15))+list(mid.range_to(end, 15))
    newcolors=[x.hex for x in colors]
    mappedcolors=[newcolors[int(idx)] for idx in objects[::-1]]
    ax.bar(y_pos * 1.5 + 1, objects[::-1], align='center', color=mappedcolors)
    ax.set_xticks(y_pos * 1.5 + 1)
    ax.set_xticklabels(worst_bylate['airport'][::-1])
    ax.set_ylim([0, 31])
    plt.xticks(rotation=-270)

    plt.savefig('worstairports_percentage.png',dpi=300)

    for r in range(len(df_)):
        if df_.iloc[r]['observations'] != 0:
            percentage_missed = (df_.iloc[r]['late'] / df_.iloc[r]['observations']) * 100
        else:
            percentage_missed = 0
        if df_.iloc[r][1] in ['GA', 'NY', 'TX', 'IL', 'FL', 'CA']:
            stato = states[df_.iloc[r][1]]
        else:
            stato = 'other'

        # Printing JS
        print('{' + '\n"city": "' + df_.iloc[r][0] + '",\n' + '"country": "' + stato + '",\n' + '"population": ' + str(
            df_.iloc[r][-1]) + ',\n' + '"percentage": ' + str(percentage_missed) + ',\n' + '"latitude": ' + str(
            df_.iloc[r][2]) + ',\n' + '"longitude": ' + str(df_.iloc[r][3]) + ',\n' + '},\n')



if __name__ == "__main__":
    main()
