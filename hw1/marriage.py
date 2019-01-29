import pandas as pd                                                     # import libs
import sqlite3
import re
from sqlalchemy import create_engine

marriage = pd.read_excel('data/state-marriage-rates-90-95-99-17.xlsx',  # read in the data to pandas dataframe, ready file
                         skiprows=4,                                    # skip rows header metadata
                         header=[0,1],                                  # set header
                         skipfooter=8,                                  # skip rows of footer metadata
                         na_values='---',                               # null values in excel file
                         usecols=10,                                    # set number of columns
                         index_col = [0])                               # set index column

marriage = marriage.stack([0,1]).reset_index()                          # reshape data by stacking to long, then reset index to new index

marriage.rename(columns={marriage.columns[0]: 'State',                  # rename columns, first column past index renamed to State
                         marriage.columns[1]: 'left',                   # second column renamed to left, for leftovers, column is dropped
                         marriage.columns[2]: 'Year',                   # third column renamed to Year
                         marriage.columns[3]: 'Marriage Rate'}          # fourth column set to Marriage Rate
                , inplace=True)                                         # true so that we don't have to set school = (copy we are returning)

marriage.drop(columns=['left'] ,inplace=True)                           # column is dropped, not needed

marriage.to_excel(excel_writer='data/marriage_cleaned_in_python.xls',   # read dataframe to excel, set file name
                sheet_name='marriage rates',                            # sheet named 'marriage rates'
                na_rep='null',                                          # treat n/a as null
                index=False)                                            # don't include pandas index

conn = sqlite3.connect('data/marriage.db')                              # create connection to db/ create db
marriage.to_sql(con=conn,                                               # Write our df 'marriage' to sql db / select connection
                name='MarriageRate',                                    # name table in db to 'MarriageRate
                if_exists='replace')                                    # replace table if one is already created
cur = conn.cursor()                                                     # create cursor object to query db
cur.execute("SELECT * FROM MarriageRate;")                              # execute query selecting all of the data in db MarrigeRate
results = cur.fetchall()                                                # set var results = to all of the data fetched
print(results)                                                          # print results / all data fetched / printing to see if db
                                                                        # and table are working








