import asset_asrl as ast
import numpy as np
import matplotlib.pyplot as plt
from astropy.time import Time
from astropy.time import TimeDelta
from astropy import units as u
from astropy import constants as const
from astropy.coordinates import solar_system_ephemeris
from astropy.coordinates import get_body_barycentric_posvel
from astropy.coordinates import get_body_barycentric

from body import *
from orbit import *
from orbit_util import *

vf = ast.VectorFunctions
oc = ast.OptimalControl
Args = vf.Arguments

result = np.load("phase1_bodies_data.npz", allow_pickle=True)
sat = result['arr_0'][()]
earth = result['arr_1'][()]
moon = result['arr_2'][()]

phase1_data = np.load("phase1_data.npy", allow_pickle=True)[()]
EarthOrbTraj = phase1_data["EarthOrbTraj"]
EarthOrbApo = phase1_data["EventLocs"][0][0]
epoch = phase1_data["epoch"]

phase2_data = np.load("phase2_data.npy", allow_pickle=True)[()]
MoonTransferTraj = phase2_data["MoonTransferTraj"]
phase2_t0 = phase2_data["t0"]

"""
Plot Earth Orbit
"""
earth_orbit = True
if earth_orbit:
    sat.r_ar = np.zeros((len(EarthOrbTraj), 3))
    sat.v_ar = np.zeros((len(EarthOrbTraj), 3))
    moon.r_ar = np.zeros((len(EarthOrbTraj), 3))
    moon.v_ar = np.zeros((len(EarthOrbTraj), 3))
    sat.t_ar = np.zeros((len(EarthOrbTraj), 1))
    earth.r_ar = np.zeros((len(EarthOrbTraj), 3))

    for i in range(len(EarthOrbTraj)):
        sat.r_ar[i] = EarthOrbTraj[i][0:3]
        sat.v_ar[i] = EarthOrbTraj[i][3:6]
        moon.r_ar[i] = EarthOrbTraj[i][6:9]
        moon.v_ar[i] = EarthOrbTraj[i][9:12]
        sat.t_ar[i] = EarthOrbTraj[i][12]

        earth.r_ar[i] = get_body_barycentric(
            earth.label, epoch+TimeDelta(EarthOrbTraj[i][12], format='sec')).xyz.to(u.km).value

        print(i)

    ax = plt.figure().add_subplot(projection='3d')

    # Plot central body
    ax.scatter(0, 0, 0, color=earth.color, s=5,
               marker='o', edgecolor='k', label=earth.label)

    # Plot Apogee Event
    ax.scatter(EarthOrbApo[0], EarthOrbApo[1], EarthOrbApo[2], color='orange', s=5,
               marker='o', edgecolor='k', label="Apogee")

    # Plot sat
    ax.plot(sat.r_ar[:, 0], sat.r_ar[:, 1], sat.r_ar[:, 2],
            color=sat.color,
            label=sat.label)

    # Plot moon
    # ax.plot(moon.r_ar[:, 0] - earth.r_ar[:, 0],
    #         moon.r_ar[:, 1] - earth.r_ar[:, 1],
    #         moon.r_ar[:, 2] - earth.r_ar[:, 2],
    #         color=moon.color,
    #         label=moon.label)

    ax.set_title(f"LEG-1: {earth.label} Frame", fontsize=14, pad=10)
    ax.set_aspect('equal')
    ax.set_xlabel("X [km]")
    ax.set_ylabel("Y [km]")
    ax.set_zlabel("Z [km]")
    ax.legend(loc='center left', bbox_to_anchor=(1.25, 0.5))
    plt.tight_layout()
    plt.savefig('earth_orbit.png', dpi=300, bbox_inches='tight')
    plt.show()

"""
Plot Earth-Moon Transfer
"""
transfer_orbit = False
if transfer_orbit:
    sat.r_ar = np.zeros((len(MoonTransferTraj), 3))
    sat.v_ar = np.zeros((len(MoonTransferTraj), 3))
    moon.r_ar = np.zeros((len(MoonTransferTraj), 3))
    moon.v_ar = np.zeros((len(MoonTransferTraj), 3))
    sat.t_ar = np.zeros((len(MoonTransferTraj), 1))
    earth.r_ar = np.zeros((len(MoonTransferTraj), 3))

    for i in range(len(MoonTransferTraj)):
        sat.r_ar[i] = MoonTransferTraj[i][0:3]
        sat.v_ar[i] = MoonTransferTraj[i][3:6]
        moon.r_ar[i] = MoonTransferTraj[i][6:9]
        moon.v_ar[i] = MoonTransferTraj[i][9:12]
        sat.t_ar[i] = MoonTransferTraj[i][12]

        start_time = epoch + \
            TimeDelta(phase2_t0, format='sec') + \
            TimeDelta(MoonTransferTraj[i][12], format='sec')

        earth.r_ar[i] = get_body_barycentric(
            earth.label, start_time).xyz.to(u.km).value

        print(i)

    ax = plt.figure().add_subplot(projection='3d')

    # Plot central body
    ax.scatter(0, 0, 0, color=earth.color, s=5,
               marker='o', edgecolor='k', label=earth.label)

    # Plot sat
    ax.plot(sat.r_ar[:, 0], sat.r_ar[:, 1], sat.r_ar[:, 2],
            color=sat.color,
            label=sat.label)

    # Plot moon
    # ax.plot(moon.r_ar[:, 0] - earth.r_ar[:, 0],
    #         moon.r_ar[:, 1] - earth.r_ar[:, 1],
    #         moon.r_ar[:, 2] - earth.r_ar[:, 2],
    #         color=moon.color,
    #         label=moon.label)

    ax.set_title(
        f"Earth-Moon Transfer: {earth.label} Frame", fontsize=14, pad=10)
    ax.set_aspect('equal')
    ax.set_xlabel("X [km]")
    ax.set_ylabel("Y [km]")
    ax.set_zlabel("Z [km]")
    ax.legend(loc='center left', bbox_to_anchor=(1.25, 0.5))
    plt.tight_layout()
    plt.savefig('earth_orbit.png', dpi=300, bbox_inches='tight')
    plt.show()


"""
Plot OCP MULTI PHASE
"""

ocp_data = np.load("ocp_data.npy", allow_pickle=True)[()]
Phase1Traj = ocp_data["Phase1Traj"]
Phase2Traj = ocp_data["Phase2Traj"]

phases = [Phase1Traj, Phase2Traj]
# phases = [Phase1Traj]
# phases = [Phase2Traj]
colors = ['blue', 'red']

ocp_plot = True
if ocp_plot:

    ax = plt.figure().add_subplot(projection='3d')

    # Plot central body
    ax.scatter(0, 0, 0, color=earth.color, s=5,
               marker='o', edgecolor='k', label=earth.label)

    for ii, phase in enumerate(phases):
        phase_len = len(phase)
        sat.r_ar = np.zeros((phase_len, 3))
        sat.v_ar = np.zeros((phase_len, 3))
        moon.r_ar = np.zeros((phase_len, 3))
        moon.v_ar = np.zeros((phase_len, 3))
        sat.t_ar = np.zeros((phase_len, 1))
        earth.r_ar = np.zeros((phase_len, 3))

        for i in range(len(phase)):
            sat.r_ar[i] = phase[i][0:3]
            sat.v_ar[i] = phase[i][3:6]
            moon.r_ar[i] = phase[i][6:9]
            moon.v_ar[i] = phase[i][9:12]
            sat.t_ar[i] = phase[i][12]

            earth.r_ar[i] = get_body_barycentric(
                earth.label, epoch+TimeDelta(phase[i][12], format='sec')).xyz.to(u.km).value

            print(i)

        # Plot sat
        ax.plot(sat.r_ar[:, 0], sat.r_ar[:, 1], sat.r_ar[:, 2],
                color=colors[ii],
                label=sat.label)

        # Plot moon
        # ax.plot(moon.r_ar[:, 0] - earth.r_ar[:, 0],
        #         moon.r_ar[:, 1] - earth.r_ar[:, 1],
        #         moon.r_ar[:, 2] - earth.r_ar[:, 2],
        #         color=moon.color,
        #         label=moon.label)

    ax.set_aspect('equal')
    ax.set_xlabel("X [km]")
    ax.set_ylabel("Y [km]")
    ax.set_zlabel("Z [km]")
    ax.legend(loc='center left', bbox_to_anchor=(1.25, 0.5))
    plt.tight_layout()
    plt.savefig('earth_orbit.png', dpi=300, bbox_inches='tight')
    plt.show()
