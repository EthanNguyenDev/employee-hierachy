import pandas as pd
import os
import numpy as np
from pprint import pprint
from collections import defaultdict
import time
import json

start_time = time.time()
print('Script starts running, pls be patient!')

dir = './'
filePath = os.path.join(dir, 'Input.xlsx')

df = pd.read_excel(filePath)
df.head()
df2 = df.copy()


def buildtree(t=None, parent_id=''):
    directReportList = mngrEmpDict.get(parent_id, None)
    if directReportList is None:
        return t
    for id in directReportList:
        report = { 'id': id }
        if t is None:
            t = report
        else:
            reports = t.setdefault('reports', [])
            reports.append(report)
        buildtree(report, id)
    return t

def prepare_emp_mngr_dict(df):
    empMngrDict = defaultdict(str)
    for index, row in df.iterrows():
        empMngrDict[row['Employee ID']] = row['BU/SU Manager ID']
    return empMngrDict

def prepare_mngr_emp_dict(empMngrDict):
    mngrEmpDict = defaultdict(str)
    for key, value in empMngrDict.items():
        emp = key
        mgr = value
        # if saw emp-emp  or emp-'' entry, it's Piyush, he has no manager, excel assume he report to himself!
        if (emp != mgr or not mgr):
            directReportList = mngrEmpDict.get(mgr, [])
            directReportList.append(emp)
            mngrEmpDict[mgr] = directReportList
        else:
            mngrEmpDict[''] = [mgr]
    return mngrEmpDict


# prepare data from Excel
empMngrDict = prepare_emp_mngr_dict(df)
# dict of manager --> list of employee
mngrEmpDict = prepare_mngr_emp_dict(empMngrDict)

# build hierachy tree
data = buildtree()
#pprint(data)

result = defaultdict(list)
def processAncestors(root, targetId):
    # Base case 
    if root.get('id') == None or not root.get('id'): 
        return False
    # current root match target  
    if root.get('id') == targetId: 
        return True 
  
    # If target is present in either left or right subtree of this node, then print this node 
    if root.get('reports') != None:
        for eachDirectReport in root.get('reports'):
            if (processAncestors(eachDirectReport, targetId)): 
                #print (root.get('id'))
                result[targetId].append(root.get('id'))
                return True
  
    # Else return False  
    return False

for key, value in empMngrDict.items():
    processAncestors(data, key)
# processAncestors(data, '012849')
# print(result)

# result = defaultdict(list)
# dir = './'
# filePath = os.path.join(dir, 'result.json')
# json1_file = open(filePath, encoding="utf8", errors='ignore')
# json1_str = json1_file.read()
# result = json.loads(json1_str)

# output to excel
print('output to excel')
for rowIndex, row in df2.iterrows():
    employeeId = row['Employee ID'] # as string
    managerHierachy = result.get(employeeId, None)
    if managerHierachy and managerHierachy != None:
        reversedManagerHierachy = list(reversed(managerHierachy))
        for i in range(0, 12):
            try:
                df2.at[rowIndex, 'L' + str(i + 1)] = managerHierachy[i]
            except IndexError:
                df2.at[rowIndex, 'L' + str(i + 1)] = ''
        # for i in range(0, 12):
        #     if ()
        #     try:
        #         df2.at[rowIndex, 'R' + str( i + 1)] = reversedManagerHierachy[i]
        #     except Exception:
        #         df2.at[rowIndex, 'R' + str(i + 1)] = ''
        
        # First few cols are from the tree
        noOfLevel = len(reversedManagerHierachy)
        # Fill in the first few cols with relevant data
        for i in range(0, noOfLevel):
            df2.at[rowIndex, 'R' + str(i + 1)] = reversedManagerHierachy[i]
        # Adding the employee himself/herself at the last level - from top-down direction
        df2.at[rowIndex, 'R' + str(noOfLevel + 1)] = employeeId
        # Fill in the rest of cols with empty string
        for i in range(noOfLevel + 2 , 13):
            df2.at[rowIndex, 'R' + str(i)] = ''
        #print('Complete {} row'.format(rowIndex))
    else:
        # Special handling for the big boss, he's reporting to himself
        df2.at[rowIndex, 'R1'] = employeeId

df2.to_excel("Output.xlsx")
print("--- %s seconds ---" % (time.time() - start_time))

