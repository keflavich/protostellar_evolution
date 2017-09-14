import numpy as np
import re
from astropy import constants, units as u, table, stats, coordinates, wcs
import pylab as pl

fig1 = pl.figure(1)
fig1.clf()
fig2 = pl.figure(2)
fig2.clf()
fig3 = pl.figure(3)
fig3.clf()

tables = {}
for mdot in np.logspace(-6, -2, 12):

    fn = 'protostellar_evolution_mdot={0}.txt'.format(mdot)
    print(fn)
    
    with open(fn, 'r') as fh:
        lines = fh.readlines()
    lines[0] = re.sub("([a-z]) ([A-Z])", "\\1_\\2", lines[0])
    with open(fn, 'w') as fh:
        fh.writelines(lines)

    tbl = table.Table.read(fn, format='ascii', )

    tables[mdot] = tbl

    ax = fig1.gca()
    ax.plot(tbl['Stellar_Mass'] / constants.M_sun.cgs.value, tbl['Stellar_Radius'] / constants.R_sun.cgs.value,
            label=mdot)
    ax.set_xlabel("Stellar Mass (M$_\odot$)")
    ax.set_ylabel("Stellar Radius (R$_\odot$)")
    pl.legend(loc='best')

    ax = fig2.gca()
    ax.plot(tbl['Stellar_Mass'] / constants.M_sun.cgs.value, tbl['Total_Luminosity'] / constants.L_sun.cgs.value,
            label=mdot)
    ax.set_xlabel("Stellar Mass (M$_\odot$)")
    ax.set_ylabel("Stellar Luminosity (L$_\odot$)")

    pl.legend(loc='best')

    ax = fig3.gca()
    ax.plot(tbl['Time'] / u.Myr.to(u.s), tbl['Stellar_Mass'] / constants.M_sun.cgs.value,
            label=mdot)
    ax.set_ylabel("Stellar Mass (M$_\odot$)")
    ax.set_xlabel("Time (Myr)")

    pl.legend(loc='best')
