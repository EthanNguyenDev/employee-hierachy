from pprint import pprint
from random import shuffle
from collections import defaultdict
import json

def show_val(title, val):
    """
    Debugging print helpler.
    """
    sep = '-' * len(title)
    print ("\n{}\n{}\n{}\n".format(sep, title, sep))
    pprint(val)


# ORIGINAL NAMES:   emp_id, emp_name, mgr_id
# SIMPLIFIED NAMES: eid,    name,     mid
text = """
323,The Boss,
4444,Manager Joe,323
3,Manager Sally,323
4,Peon Frank,4444
33,Peon Dave,3
5,Peon Jill,4444
6,Peon Rodger,3
7,Peon Ralph,3
233,Clerk Jane,99
99,Supervisor Henri,3
"""

# parse text into lines
lines = [ l.strip() for l in text.strip().splitlines() ]

# construct list of people tuples
people = [ tuple(l.split(',')) for l in lines ]

# for demonstration and testing only, shuffle the results
shuffle(people)
show_val("randomized people", people)

# contstruct list of parents
parents = defaultdict(list)
for p in people:
    parents[p[2]].append(p)
show_val("parents", parents)

def buildtree(t=None, parent_eid=''):
    """
    Given a parents lookup structure, construct
    a data hierarchy.
    """
    parent = parents.get(parent_eid, None)
    if parent is None:
        return t
    for eid, name, mid in parent:
        report = { 'name': name }
        if t is None:
            t = report
        else:
            reports = t.setdefault('reports', [])
            reports.append(report)
        buildtree(report, eid)
    return t

data = buildtree()
show_val("data", data)

show_val("JSON", json.dumps(data))