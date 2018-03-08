import numpy as np
from matplotlib import pyplot as plt
from collections import namedtuple

import payload
import unavail_mass

g_0 = 9.81

Technology = namedtuple('Technology', ['name', 'c_1', 'c_2', 'E_1', 'E_2', 'y'])
kerosene_tech = Technology(name='kerosene',
    c_1=297*g_0, E_1=0.060, c_2=350*g_0, E_2=0.040, y=0.265)
hydrogen_tech = Technology(name='hydrogen',
    c_1=386*g_0, E_1=0.121, c_2=462*g_0, E_2=0.120, y=0.18)


class Strategy(object):
    def __init__(self, landing_method, recov_location, z_m, technology, a, P):
        """A recovery strategy.

        a and P should be tuples, with a[0], P[0] representing the
        optimistic extreme of the estimated range, and [1] the pessimistic extreme.
        """
        assert landing_method in ('Propulsive', 'Winged', 'Parachute')
        self.landing_method = landing_method

        assert recov_location in ('Launch Site', 'Downrange')
        self.recov_location = recov_location

        assert z_m >= 0 and z_m <= 1
        self.z_m = z_m

        self.technology = technology

        assert len(a) == 2
        assert a[0] >= 0 and a[1] >= 0
        assert a[0] < 1 and a[1] < 1
        self.a = a

        assert len(P) == 2
        assert P[0] >= 0 and P[1] >= 0
        self.P = P


    def get_payload_expend(self, dv_mission):
        """Get the payload mass fraction of the equivalent expendable vehicle."""
        return payload.payload_fixed_stages(
            self.technology.c_1,
            self.technology.c_2,
            self.technology.E_1,
            self.technology.E_2,
            self.technology.y,
            dv_mission
            )

    def get_unavail_mass(self, which_extreme=0):
        """Get the first stage unavailable mass fraction."""
        return unavail_mass.unavail_mass(
            self.a[which_extreme],
            self.P[which_extreme],
            self.z_m,
            self.technology.E_1
            )

    def get_payload_recov(self, dv_mission, which_extreme=0):
        """Get the payload mass fraction with recovery."""
        e_1 = self.get_unavail_mass(which_extreme)
        return payload.payload_fixed_stages(
            self.technology.c_1,
            self.technology.c_2,
            e_1,
            self.technology.E_2,
            self.technology.y,
            dv_mission
            )

    def get_payload_factor_range(self, dv_mission):
        """Get the payload factor r_p for a recovery strategy."""
        pi_star_expend = self.get_payload_expend(dv_mission)
        pi_star_recov_hi = self.get_payload_recov(dv_mission, 0)
        pi_star_recov_lo = self.get_payload_recov(dv_mission, 1)

        r_p = (pi_star_recov_hi / pi_star_expend, pi_star_recov_lo / pi_star_expend)
        return r_p


def main():
    landing_colors = {'Propulsive': 'red', 'Winged':'blue', 'Parachute':'Green'}
    location_colors = {'Launch Site': 'green', 'Downrange':'blue'}

    dv_mission = 9.5e3

    prop_ls = Strategy(landing_method='Propulsive', recov_location='Launch Site',
        z_m=1.0, technology=kerosene_tech,
        a=(0.05, 0.07), P=np.array([2700, 3800+500]) / kerosene_tech.c_1)
    prop_dr = Strategy(landing_method='Propulsive', recov_location='Downrange',
        z_m=1.0, technology=kerosene_tech,
        a=(0.05, 0.07), P=np.array([800, 1150]) / kerosene_tech.c_1)

    glider = Strategy(landing_method='Winged', recov_location='Downrange',
        z_m=1.0, technology=kerosene_tech,
        a=(0.18, 0.37), P=(0, 0))
    flyback = Strategy(landing_method='Winged', recov_location='Launch Site',
        z_m=1.0, technology=kerosene_tech,
        a=(0.28, 0.52), P=(0.17, 0.26))

    partial_parachute = Strategy(landing_method='Parachute', recov_location='Downrange',
        z_m=0.25, technology=kerosene_tech,
        a=(0.15, 0.19), P=(0, 0))

    strats = [prop_ls, prop_dr, glider, flyback, partial_parachute]
    r_p_hi = np.zeros(len(strats))
    r_p_lo = np.zeros(len(strats))
    colors = []
    edgecolors = []
    tick_labels = []

    for i in range(len(strats)):
        r_p = strats[i].get_payload_factor_range(dv_mission)
        r_p_hi[i] = r_p[0]
        r_p_lo[i] = r_p[1]
        colors.append(landing_colors[strats[i].landing_method])
        edgecolors.append(location_colors[strats[i].recov_location])
        tick_labels.append(strats[i].landing_method + '\n' + strats[i].recov_location)

    plt.bar(range(len(strats)),
        height=(r_p_hi - r_p_lo), bottom=r_p_lo,
        color=colors, edgecolor=edgecolors, tick_label=tick_labels)
    plt.ylim([0, 1])
    plt.ylabel('Payload factor $r_p$ [-]')
    plt.show()

if __name__ == '__main__':
    main()