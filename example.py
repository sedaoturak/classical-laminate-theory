"""
Example script for composits laminaties and their homoginization.

This file calculates the properties of simple composite plates.
The stacking sequence should be defined starting from the top of the laminate,
which is the negative :math:`z` direction.

A.J.J. Lagerweij
COHMAS Mechanical Engineering KAUST
2020
"""

# Import external packages.
import numpy as np

# Import local packages.
import homogenization
import abdcal
import deformation
import failure


###############################################################################
# Ply Properties                                                              #
###############################################################################
# List the elastic properties of the ply. (Std CF/epoxy)
El = 142 * 1e3  # Elastic modulus in longitudinal direction, MPa 
Et = 13 * 1e3  # Elastic modulus in transverse direction, MPa
G = 5 * 1e3  # Shear Modulus, MPa
nult = 0.3  # Poisson's Ratio

# List the failure properties of the ply.
Xt = 2200  # MPa
Xc = 1850  # MPa
Yt = 55  # MPa
Yc = 200  # MPa
Smax = 120  # MPa

# List the other properties of the ply.
t = 0.16 # mm -cured ply thickness

# Calculate the ply stiffness matricess matrix.
Q = abdcal.QPlaneStress(El, Et, nult, G)


###############################################################################
# Laminate Properites                                                         #
###############################################################################
# Define the stacking sequence.

import json
with open('all_layup_designs_10layer.json', 'r') as f:
  layup_designs = json.load(f) #keys in order: bs, ubs, bus, ubus

bs = layup_designs['bs']

angles_deg = [0, 0, -45, 90, -45, -45, 90, 45, 0, 0]
thickness = [t] * len(angles_deg)
Q = [Q] * len(angles_deg)

# Calculate the ABD matrix and its inverse.
abd = abdcal.abd(Q, angles_deg, thickness)
abd_inv = abdcal.matrix_inverse(abd)


###############################################################################
# Applied Running Loads                                                       #
###############################################################################
# Calculate the deformation caused by a given running load.
NM = np.matrix([0, 1, 0, 1, 0, 0]).T  # MPa/mm and MPa*mm/mm
deformed = deformation.load_applied(abd_inv, NM)

# Calculate the stress in each layer caused by the running loads.
strain = deformation.ply_strain(deformed, Q, angles_deg, thickness)
stress = deformation.ply_stress(deformed, Q, angles_deg, thickness, plotting=True)


strs_list = []
for strs in stress:
  strs_list.append(strs[0].tolist()+strs[1].tolist())

all_stresses = []
for strs in strs_list:
  mid_list = []
  for strs2 in strs:
    mid_list.append(strs2[0])
  all_stresses.append(mid_list)

import time
timestr = time.strftime("%Y%m%d-%H%M%S")

import json
with open(f'/content/drive/My Drive/all_simulations_10layer_{timestr}.json', 'w') as files:
    json.dump(all_stresses, files)

###############################################################################
# Test Ply Failure with various criteria                                      #
###############################################################################
# Testing whether the failure criterias are violated.
# failure.max_stress(stress, Xt, Xc, Yt, Yc, Smax)
# failure.tsai_wu(stress, Xt, Xc, Yt, Yc, Smax)
# failure.tsai_hill(stress, Xt, Xc, Yt, Yc, Smax)
