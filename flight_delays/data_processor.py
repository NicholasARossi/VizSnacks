import pandas as pd
import numpy as np


def main():
    """ This function processes all the data and outputs a javascript object that can be read by the associated .js file"""
    df = pd.read_json('delays.json')
    keys = pd.read_csv('ICAO_airports.csv', error_bad_lines=False, encoding="ISO-8859-1")

    codes = df['icao code'].unique()
    columns = ['code', 'state', 'lat', 'long', 'delay15', 'delay30', 'delay45', 'observations', 'ontime']
    df_ = pd.DataFrame(columns=columns)

    for code in codes:
        slico = df[df['icao code'] == code]
        lat, long = keys[keys['ident'] == code]['latitude_deg'], keys[keys['ident'] == code]['longitude_deg']
        state = list(keys[keys['ident'] == code]['iso_region'])[0].split('-')[1]
        df2 = pd.DataFrame([[code, state, float(lat), float(long), sum(slico['delayed15']), sum(slico['delayed30']),
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
