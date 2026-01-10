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
from Orbit_util import *

vf = ast.VectorFunctions
oc = ast.OptimalControl
Args = vf.Arguments


result = np.load("mission_data.npz", allow_pickle=True)
sat = result['arr_0'][()]
earth = result['arr_1'][()]
moon = result['arr_2'][()]

leg_1_data = np.load("leg_1_data.npy", allow_pickle=True)[()]
TrajExact = leg_1_data["TrajExact"]

sat.r_ar = np.zeros((len(TrajExact), 3))
sat.v_ar = np.zeros((len(TrajExact), 3))
moon.r_ar = np.zeros((len(TrajExact), 3))
moon.v_ar = np.zeros((len(TrajExact), 3))
sat.t_ar = np.zeros((len(TrajExact), 1))

for i in range(len(TrajExact)):
    sat.r_ar[i] = TrajExact[i][0:3]
    sat.v_ar[i] = TrajExact[i][3:6]
    moon.r_ar[i] = TrajExact[i][6:9]
    moon.v_ar[i] = TrajExact[i][9:12]
    sat.t_ar[i] = TrajExact[i][12]

ax = plt.figure().add_subplot(projection='3d')

# Plot central body
ax.scatter(0, 0, 0, color=earth.color, s=5,
           marker='o', edgecolor='k', label=earth.label)

# Plot sat
ax.plot(sat.r_ar[:, 0], sat.r_ar[:, 1], sat.r_ar[:, 2],
        color=sat.color,
        label=sat.label)


# Plot moon
# ax.plot(moon.r_ar[:, 0], moon.r_ar[:, 1], moon.r_ar[:, 2],
#    color=moon.color,
#    label=moon.label)

ax.set_title(f"LEG-1: {earth.label} Frame", fontsize=14, pad=10)
ax.set_aspect('equal')
ax.set_xlabel("X [km]")
ax.set_ylabel("Y [km]")
ax.set_zlabel("Z [km]")
ax.legend(loc='center left', bbox_to_anchor=(1.25, 0.5))
plt.tight_layout()
plt.savefig('earth_orbit.png', dpi=300, bbox_inches='tight')
plt.show()
