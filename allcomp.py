import pandas as pd
from pathlib import Path


def excel_diff(path_polbnc, path_ref, index_col_pbc, index_col_ref):

    global df_polbnc, dfdiff, cols_polbnc, cols_pol, cols_bil, df_pol, df_bil, newRows, droppedRows, dfdiff
    df_polbnc = pd.read_excel(path_polbnc, index_col=index_col_pbc).fillna(0)

    # Perform Diff
    dfdiff = df_polbnc.copy()
    cols_polbnc = df_polbnc.columns
    # print('cols_polbnc type :', cols_polbnc)

    path_temp = str(path_ref)[0:3]
    if path_temp == 'BIL':
        df_bil = pd.read_excel(path_ref, index_col=index_col_ref).fillna(0)
        df_bil = df_bil.rename(
            columns={
                "PAYMENT STATUS": "BILLING STATUS",
                "FREQUENCY": "BILLING FREQUENCY"
            }
        )
        cols_bil = df_bil.columns
    elif path_temp == 'POL':
        df_pol = pd.read_excel(path_ref, index_col=index_col_ref).fillna(0)
        df_pol = df_pol.rename(
            columns={
                "AGE": "ISSUE AGE"
            }
        )
        cols_pol = df_pol.columns
    # return cols_polbnc


def excel_cmp(cols_polbnc, cols_ref, df_ref, df_polbnc, dfdiff):

#    global df_polbnc, dfdiff, cols_polbnc, cols_pol, cols_bil, df_pol, df_bil, newRows, droppedRows, dfdiff
    droppedRows = []
    newRows = []
    sharedCols = list(set(cols_polbnc).intersection(cols_ref))

    for row in dfdiff.index:
        if (row in df_polbnc.index) and (row in df_ref.index):
            for col in sharedCols:
                value_polbnc = df_polbnc.loc[row,col]
                value_ref = df_ref.loc[row,col]
                if value_polbnc==value_ref:
                    dfdiff.loc[row,col] = df_ref.loc[row,col]
                else:
                    dfdiff.loc[row,col] = ('{}→{}').format(value_polbnc,value_ref)
        else:
            newRows.append(row)

    for row in df_polbnc.index:
        if row not in df_ref.index:
            droppedRows.append(row)
            dfdiff = dfdiff.append(df_polbnc.loc[row,:])

    dfdiff = dfdiff.sort_index().fillna('')
#    print(dfdiff)
    print('\nNew Rows:     {}'.format(newRows))
    print('Dropped Rows: {}'.format(droppedRows))

    # Save output and format
#    fname = '{} vs {}.xlsx'.format(path_polbnc.stem,path_bil.stem)
    fname = 'POLBNC_compare.xlsx'
    writer = pd.ExcelWriter(fname, engine='xlsxwriter')

    dfdiff.to_excel(writer, sheet_name='DIFF', index=True)
#    df_bil.to_excel(writer, sheet_name=path_bil.stem, index=True)
#    df_polbnc.to_excel(writer, sheet_name=path_polbnc.stem, index=True)

    # get xlsxwriter objects
    workbook  = writer.book
    worksheet = writer.sheets['DIFF']
    worksheet.hide_gridlines(2)
    worksheet.set_default_row(15)

    # define formats
    date_fmt = workbook.add_format({'align': 'center', 'num_format': 'yyyy-mm-dd'})
    center_fmt = workbook.add_format({'align': 'center'})
    number_fmt = workbook.add_format({'align': 'center', 'num_format': '#,##0.00'})
    cur_fmt = workbook.add_format({'align': 'center', 'num_format': '$#,##0.00'})
    perc_fmt = workbook.add_format({'align': 'center', 'num_format': '0%'})
    grey_fmt = workbook.add_format({'font_color': '#E0E0E0'})
    highlight_fmt = workbook.add_format({'font_color': '#FF0000', 'bg_color':'#B1B3B3'})
    new_fmt = workbook.add_format({'font_color': '#32CD32','bold':True})

    # set format over range
    ## highlight changed cells
    worksheet.conditional_format('A1:ZZ1000', {'type': 'text',
                                            'criteria': 'containing',
                                            'value':'→',
                                            'format': highlight_fmt})

    # highlight new/changed rows
    for row in range(dfdiff.shape[0]):
        if row+1 in newRows:
            worksheet.set_row(row+1, 15, new_fmt)
        if row+1 in droppedRows:
            worksheet.set_row(row+1, 15, grey_fmt)

    # save
    writer.save()
    print('\nDone.\n')


path_polbnc = Path('POLBNC_sample.xlsx')
path_bil = Path('BIL_sample.xlsx')
path_pol = Path('POL_sample.xlsx')

# get index col from data
dfpbc = pd.read_excel(path_polbnc)
dfbil = pd.read_excel(path_bil)
dfpol = pd.read_excel(path_pol)
index_col_pbc = dfpbc.columns[7]
index_col_bil = dfbil.columns[1]
index_col_pol = dfpol.columns[5]

print('\nIndex column: {}'.format(index_col_pbc))
print('\nIndex column: {}'.format(index_col_bil))
print('\nIndex column: {}'.format(index_col_pol))

excel_diff(path_polbnc, path_bil, index_col_pbc, index_col_bil)
excel_cmp(cols_polbnc, cols_bil, df_bil, df_polbnc, dfdiff)
excel_diff(path_polbnc, path_pol, index_col_pbc, index_col_pol)
excel_cmp(cols_polbnc, cols_pol, df_pol, df_polbnc, dfdiff)