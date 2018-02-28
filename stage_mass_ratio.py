"""Effect of stage mass ratio on payload capacity."""

import numpy as np
from matplotlib import pyplot as plt

import payload

def main():
    g_0 = 9.81
    # Stage exahust velocities [units: meter second**-1].
    # O2/kerosene
    c_1 = 290 * g_0
    c_2 = 350 * g_0

    # Stage inert mass fractions
    e_1_steps = np.linspace(0.10, 0.25, 4)
    e_2 = 0.08

    # Stage mass ratio [units: dimensionless].
    y = np.linspace(0.05, 0.50)

    # Mission delta-v [units: meter second**-1].
    # dv_mission = 12e3    # GTO
    dv_mission = 9.5e3    # LEO

    for e_1 in  e_1_steps:
        pi_star = np.zeros(y.shape)
        for i in range(len(y)):
            pi_star[i] = payload.payload_fixed_stages(
                c_1, c_2, e_1, e_2, y[i], dv_mission)
        plt.plot(y, pi_star, label="$\\epsilon_1'=${:.2f}".format(e_1))
        i_max = np.nanargmax(pi_star)
        if (i_max != 0) and (i_max != len(y) - 1):
            plt.scatter(y[i_max], pi_star[i_max])

    plt.legend()
    plt.xlabel("2nd/1st stage mass ratio $y$ [-]")
    plt.ylabel('Payload mass fraction $\\pi_*$ [-]')
    plt.title("Effect of $\\epsilon_1'$ on optimal stage mass ratio\n"
        + 'for $$c_1/g_0$={:.0f} s, c_2/g_0$={:.0f} s,'.format(c_1/g_0, c_2/g_0)
        + '$\\epsilon_2$={:.2f}, $\Delta v_*$={:.1f} km/s'.format(e_2, dv_mission * 1e-3))
    # Start plot at 0,0
    ax = plt.gca()
    ax.set_xlim(xmin=0)
    ax.set_ylim(ymin=0)
    plt.show()


if __name__ == '__main__':
    main()