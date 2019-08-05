import pandas as pd
import os
import sys
import numpy as np

print('Script starts running, pls be patient!')
dir = './'
filePath = os.path.join(dir, 'Python_trial data.xlsx')

df = pd.read_excel(filePath)
df.head()
# adding empty column as result
df2 = df.copy()
#df2['totalSpan'] = np.zeros(len(df['Employee ID']))
result = {}

def populateResultUtil(mngr, mngrEmpMap):
    global result
    count = 0
    # means employee is not a manager of any other employee
    if mngr not in mngrEmpMap:
        result[mngr] = 0
        return 0
    # this employee count has already been done by this
    # method, so avoid re-computation
    elif mngr in result:
        count = result.get(mngr)
    else:
        directReportEmpList = mngrEmpDict.get(mngr, [])
        count = len(directReportEmpList)
        for directReportEmp in directReportEmpList:
            count += populateResultUtil(directReportEmp, mngrEmpMap)
        result[mngr] = count
    return count

empMngrDict = {}

for index, row in df.iterrows():
    empMngrDict[row['Employee ID']] = row['BU/SU Manager ID']

# dict of manager --> employee list
mngrEmpDict = {}
for key, value in empMngrDict.items():
    emp = key
    mgr = value
    # excluding emp-emp entry
    if (emp != mgr):
        directReportList = mngrEmpDict.get(mgr, [])
        directReportList.append(emp)
        mngrEmpDict[mgr] = directReportList

#print(mngrEmpDict)


# loop over emp-manager map & will use mngr-emp map in helper to get the count

for key, value in empMngrDict.items():
    populateResultUtil(key, mngrEmpDict)

#print(result)

for index, row in df.iterrows():
    count = result.get(row['Employee ID'], None)
    if count is None:
        df2.loc[index, 'totalSpan'] = -1
    else:
        df2.loc[index, 'totalSpan'] = count

    directReportList = mngrEmpDict.get(row['Employee ID'], None)
    if directReportList is None:
        directReportCount = 0
    else:
        directReportCount = len(directReportList)

    if directReportCount is None:
        df2.loc[index, 'directReportCount'] = -1
    else:
        df2.loc[index, 'directReportCount'] = directReportCount
        if count is not None:
            df2.loc[index, 'indirectReportCount'] = count - directReportCount

df2.to_excel("output_count.xlsx")

