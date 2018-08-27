"""Cost per flight model for Delta IV rocket."""
import math
import matplotlib.pyplot as plt
import rhodium as rdm
import sys
import os
sys.path.append(os.path.abspath('..'))
from tools import cost_reduction_factor
from elements import ExpendableBallisticStageStorable, SolidPropellantVehicleStage, StorableTurboFed
from vehicle import LaunchVehicle

core = ExpendableBallisticStageStorable("s1", 18800 - 2 * 2350) # stage - engines, from spacelaunchreport,
core_engine = StorableTurboFed("e1", 2350) # from russianspaceweb
stage2 = SolidPropellantVehicleStage("s2", 2100 + 972) # stage + fairing, from Isakowitz

antares_elements = [core, core_engine, stage2]
antares230 = LaunchVehicle(name='antares230', M0=286, N=2, element_list=antares_elements) # mass from spacelaunchreport
antares_engines_dict = {'e1': 2}
antares_f8_dict = {'s1': 1.0, 'e1': 1.49, 's2': 1.0, 'veh': 1.0}

antares_uncertainty_list = [
    rdm.TriangularUncertainty('p_s1', min_value=0.75, mode_value=0.8, max_value=0.85),
    rdm.TriangularUncertainty('p_e1', min_value=0.75, mode_value=0.8, max_value=0.85),
    rdm.TriangularUncertainty('p_s2', min_value=0.75, mode_value=0.8, max_value=0.85),
    rdm.TriangularUncertainty('f0_prod_veh', min_value=1.02, mode_value=1.025, max_value=1.03),
    rdm.TriangularUncertainty('f9_veh', min_value=1.03, mode_value=1.04, max_value=1.05),
    rdm.TriangularUncertainty('f10_s1', min_value=0.75, mode_value=0.8, max_value=0.85),
    rdm.TriangularUncertainty('f10_e1', min_value=0.75, mode_value=0.8, max_value=0.85),
    rdm.TriangularUncertainty('f10_s2', min_value=0.75, mode_value=0.8, max_value=0.85),
]

antares_prod_nums = range(1, 10)