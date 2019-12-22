import pandas as pd
from pathlib import Path
# from txt_to_xcl import txt_excel as t
import txt_to_xcl as t


def col_rename(typ_ref, index_col_ref):

    global cols_pol, cols_bil, df_pol, df_bil

    path_temp = str(typ_ref)[0:3]
    if path_temp == 'BIL':
        #df_bil = pd.read_excel(path_ref, index_col=index_col_ref).fillna(0)
        t.dfbil = t.dfbil.rename(
            columns={
                "PAYMENT STATUS": "BILLING STATUS",
                "FREQUENCY": "BILLING FREQUENCY"
            }
        )
        cols_bil = t.dfbil.columns
    elif path_temp == 'POL':
        #df_pol = pd.read_excel(path_ref, index_col=index_col_ref).fillna(0)
        t.dfpol = t.dfpol.rename(
            columns={
                "AGE": "ISSUE AGE"
            }
        )
        cols_pol = t.dfpol.columns


def excel_cmp(cols_polbnc, cols_ref, df_ref, dfdiff, df_polbnc):

    global newRows, droppedRows
    droppedRows = []
    newRows = []
    sharedCols = list(set(cols_polbnc).intersection(cols_ref))
    print('sharedCols :', sharedCols)
    print('cols_polbnc: ', cols_polbnc)
    print('cols_ref: ', cols_ref)

    for row in dfdiff.index:
        if (row in dfdiff.index) and (row in df_ref.index):
            for col in sharedCols:
                value_polbnc = dfdiff.loc[row,col]
                value_ref = df_ref.loc[row,col]
                if value_polbnc==value_ref:
                    dfdiff.loc[row,col] = df_ref.loc[row,col]
                else:
                    dfdiff.loc[row,col] = ('{}→{}').format(value_polbnc,value_ref)
        else:
            newRows.append(row)

    for row in dfdiff.index:
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

temp = t.txt_excel()

col_rename(t.str_bil, t.index_col_bil)
# print('--->',t.cols_pbc)
# print('--->',cols_bil)
# print('--->',t.dfbil)
# print('--->',t.dfdf)
# print('--->',t.df_pbc)
excel_cmp(t.cols_pbc, cols_bil, t.dfbil, t.dfdf, t.df_pbc)

col_rename(t.str_pol, t.index_col_pol)
excel_cmp(t.cols_pbc, cols_pol, t.dfpol, t.dfdf, t.df_pbc)