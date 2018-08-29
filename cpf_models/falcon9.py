"""Cost per flight model for Falcon 9 rocket."""
import math
import matplotlib.pyplot as plt
import rhodium as rdm
import sys
import os
sys.path.append(os.path.abspath('..'))
from tools import cost_reduction_factor
from elements import ExpendableBallisticStageStorable, ModernTurboFed
from vehicle import LaunchVehicle

core = ExpendableBallisticStageStorable("s1", 27200 - 9 * 470) # stage - 9 engines, from space launch report, wikipedia
core_engine = ModernTurboFed("e1", 470) # 
stage2 = ExpendableBallisticStageStorable("s2", 4500 + 1900 - 470) # stage + fairing - engine, from spaceflight101, space launch report
stage2_engine = ModernTurboFed("e2", 470) # 

falcon_elements = [core, core_engine, stage2, stage2_engine]

falcon9_block3 = LaunchVehicle(name='Falcon9_Block3', M0=459.054, N=2, element_list=falcon_elements) # mass from spaceX website
falcon9_engines_dict = {'e1': 9, 'e2': 1}
falcon9_f8_dict = {'s1': 1.0, 'e1': 1.0, 's2': 1.0, 'e2': 1.0, 'veh': 1.0, 'ops': 1.0}
falcon_uncertainty_list = [
    rdm.TriangularUncertainty('p_s1', min_value=0.75, mode_value=0.8, max_value=0.85),
    rdm.TriangularUncertainty('p_e1', min_value=0.75, mode_value=0.8, max_value=0.85),
    rdm.TriangularUncertainty('p_s2', min_value=0.75, mode_value=0.8, max_value=0.85),
    rdm.TriangularUncertainty('p_e2', min_value=0.75, mode_value=0.8, max_value=0.85),
    rdm.TriangularUncertainty('f0_prod_veh', min_value=1.02, mode_value=1.025, max_value=1.03),
    rdm.TriangularUncertainty('f9_veh', min_value=1.01, mode_value=1.02, max_value=1.03),
    rdm.TriangularUncertainty('f11_s1', min_value=0.45, mode_value=0.5, max_value=0.55),
    rdm.TriangularUncertainty('f11_e1', min_value=0.45, mode_value=0.5, max_value=0.55),
    rdm.TriangularUncertainty('f11_s2', min_value=0.45, mode_value=0.5, max_value=0.55),
    rdm.TriangularUncertainty('f11_e2', min_value=0.45, mode_value=0.5, max_value=0.55),
    rdm.TriangularUncertainty('f10_s1', min_value=0.75, mode_value=0.8, max_value=0.85),
    rdm.TriangularUncertainty('f10_e1', min_value=0.75, mode_value=0.8, max_value=0.85),
    rdm.TriangularUncertainty('f10_s2', min_value=0.75, mode_value=0.8, max_value=0.85),
    rdm.TriangularUncertainty('f10_e2', min_value=0.75, mode_value=0.8, max_value=0.85),
]

falcon_ops_uncertainty_list = [
    rdm.TriangularUncertainty('launch_rate', min_value=10, mode_value=18, max_value=25),
    rdm.TriangularUncertainty('p_ops', min_value=0.8, mode_value=0.85, max_value=0.9),
    rdm.TriangularUncertainty('insurance', min_value=1, mode_value=2, max_value=3),
    rdm.TriangularUncertainty('f11_ops', min_value=0.45, mode_value=0.5, max_value=0.55),
]

falcon_prod_nums = range(35, 46)
falcon_launch_nums = range(50, 61)
falcon_fv = 0.8
falcon_fc = 0.7
falcon_sum_QN = 0.8
falcon_launch_provider_type = 'C'

falcon_props_dict = {'RP-1': 90234, 'LOX': 197904 * 1.6} # volumes from spaceflight101.net
