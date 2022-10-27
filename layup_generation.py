import numpy as np
import copy
from itertools import product

n_layers = 10
layups_all = np.array(list(product([0,90,-45,45], repeat=n_layers)))

def choose_design(design):
  """Choose which lay-up design will be generated: 1:'balanced-symmetric
  2: unbalanced-symmetric', 3: balanced-unsymmetric', 4: unbalanced-unsymmetric'"""
  while design in [1,2,3,4]:

    n_first_half = n_layers//2
    if n_layers%2==0: n_second_half=n_first_half 
    else: n_second_half=n_first_half+1

    layups = []

    for layup in layups_all:
      if design==1:
        if layup.sum()==0 and np.allclose(layup[:n_first_half], np.flip(layup[n_second_half:])):
          layups.append(layup.tolist())
      elif design==2:
        if layup.sum()!=0 and np.allclose(layup[:n_first_half], np.flip(layup[n_second_half:])):
          layups.append(layup.tolist())
      elif design==3:
        if layup.sum()==0 and np.allclose(layup[:n_first_half], np.flip(layup[n_second_half:]))==False:
          layups.append(layup.tolist())
      elif design==4:
        if layup.sum()!=0 and np.allclose(layup[:n_first_half], np.flip(layup[n_second_half:]))==False:
          layups.append(layup.tolist())
  
    return layups
  else: print('There is no other design. Please enter one of these: 1,2,3,4.')

# get designs in each type
bs = choose_design(1)
ubs = choose_design(2)
bus = choose_design(3)
ubus = choose_design(4)

# collect all designs as groups in a dictionary
layup_design_groups = {
    'balanced-symmetric': bs,
    'unbalanced-symmetric': ubs,
    'balanced-unsymmetric': bus,
    'unbalanced-unsymmetric': ubus
}

# save designs
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

import json
with open(f'/all_layup_designs_10layer_{timestr}.json', 'w') as files:
    json.dump(layup_design_groups, files)