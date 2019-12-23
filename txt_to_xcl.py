from pathlib import Path

import pandas as pd


def txt_excel():

    global index_col_bil, dfbil, str_bil, index_col_pol, dfpol, str_pol, dfdf, cols_pbc, dfpbc

    str_pol = 'POL_s.txt'
    str_bil = 'BIL_s.txt'
    str_pbc = 'POLBNC_s.txt'

    df1 = pd.read_csv(str_pbc, sep='|')
    df1.to_excel('POLBNC_S1.xlsx', 'Sheet1', index = True)
    df2 = pd.read_csv(str_bil, sep='|')
    df2.to_excel('BIL_S1.xlsx', 'Sheet1', index = True)
    df3 = pd.read_csv(str_pol, sep='|')
    df3.to_excel('POL_S1.xlsx', 'Sheet1', index = True)

    dfpbc = pd.read_excel('POLBNC_S1.xlsx')
    dfbil = pd.read_excel('BIL_S1.xlsx')
    dfpol = pd.read_excel('POL_S1.xlsx')
    index_col_pbc = dfpbc.columns[1]
    index_col_bil = dfbil.columns[2]
    index_col_pol = dfpol.columns[2]

    # df_pbc = pd.read_excel('POLBNC_S1.xlsx', index_col=index_col_pbc).fillna(0)

# Perform Diff
    dfdf = dfpbc.copy()
    cols_pbc = dfdf.columns
    print('\nIndex column of POLBNC: {}'.format(index_col_pbc))
    print('\nIndex column of BIL: {}'.format(index_col_bil))
    print('\nIndex column of POL: {}'.format(index_col_pol))