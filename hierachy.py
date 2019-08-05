import boto3
import pandas as pd
import os
import sys

import time
start_time = time.time()

dir = './'
filePath = os.path.join(dir, 'Input.xlsx')
df = pd.read_excel(filePath)

def search_manager(target_column, new_column):
    a = []
    for index, row in df.iterrows():
        idx = df['Employee ID'] == row[target_column]
        res = df[idx]['BU/SU Manager ID'].values
        a.append('' if not (res and res.size > 0) else res[0])
    df[new_column] = a

search_manager('BU/SU Manager ID', 'l2')
search_manager('l2', 'l3')
#search_manager('l3', 'l4')
#search_manager('l4', 'l5')
#search_manager('l5', 'l6')
#search_manager('l6', 'l7')
#search_manager('l7', 'l8')
#search_manager('l8', 'l9')

df.to_excel("Output1.xlsx")
print("--- %s seconds ---" % (time.time() - start_time))
