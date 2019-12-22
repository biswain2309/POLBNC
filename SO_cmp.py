import pandas as pd
from pathlib import Path

def excel_diff(path_OLD, path_NEW):
    df_OLD = pd.read_excel(path_OLD).fillna(0)
    df_NEW = pd.read_excel(path_NEW).fillna(0)
#    data1 = pd.read_excel(df_OLD)
#    data2 = pd.read_excel(df_NEW)
    mask=df_OLD.FREQUENCY.isin(df_NEW.FREQUENCY.tolist())
    data_equal=df_OLD[mask]
    data_diff=df_OLD[~mask]
    dfDiff = df_OLD.copy()
#   for row in range(dfDiff.shape[0]):
    for col in range(dfDiff.shape[1]):
         try:
            value_OLD = data_diff.iloc[row, col]
            value_NEW = df_OLD.iloc[row,col]
            if value_OLD!=value_NEW:
                dfDiff.iloc[row,col] = ('{}-->{}').format(value_OLD,value_NEW)
                print(dfDiff)
         except:
             dfDiff.iloc[row,col] = ('{}-->{}').format(value_OLD, 'NaN')

    fname = '{} vs {}.xlsx'.format(path_OLD.stem,path_NEW.stem)
    writer = pd.ExcelWriter(fname, engine='xlsxwriter')

    dfDiff.to_excel(writer, sheet_name='DIFF', index=False)
    df_NEW.to_excel(writer, sheet_name=path_NEW.stem, index=False)
    df_OLD.to_excel(writer, sheet_name=path_OLD.stem, index=False)

  # get xlsxwriter objects
    workbook  = writer.book
    worksheet = writer.sheets['DIFF']
    worksheet.hide_gridlines(2)

  # define formats
    date_fmt = workbook.add_format({'align': 'center', 'num_format': 'yyyy-mm-dd'})
    center_fmt = workbook.add_format({'align': 'center'})
    number_fmt = workbook.add_format({'align': 'center', 'num_format': '#,##0.00'})
    cur_fmt = workbook.add_format({'align': 'center', 'num_format': '$#,##0.00'})
    perc_fmt = workbook.add_format({'align': 'center', 'num_format': '0%'})
    grey_fmt = workbook.add_format({'font_color': '#E0E0E0'})
#   highlight_fmt = workbook.add_format({'font_color': '#FF0000', 'bg_color':'#B1B3B3'})

    # set column width and format over columns
    # worksheet.set_column('J:AX', 5, number_fmt)

    # set format over range
    ## highlight changed cells
    worksheet.conditional_format('A2:E3', {'type': 'text',
                                          'criteria': 'containing',
                                          'value':'→',
                                          'format': highlight_fmt})
  ## highlight unchanged cells
    worksheet.conditional_format('A2:E3', {'type': 'text',
                                          'criteria': 'not containing',
                                          'value':'→',
                                          'format': grey_fmt})

    # save
    writer.save()
    print('Done.')

path_OLD = Path('my_file.xlsx')
path_NEW = Path('my_file1.xlsx')
excel_diff(path_OLD, path_NEW)