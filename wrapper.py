import numpy as np
import os
import shutil

def write_params(mdot=1e-4, ntimestep=1000, fulltime=None, mf=100):

    if fulltime is None:
        fulltime = mf / mdot

    timestep = fulltime / ntimestep

    with open('Driver.F90', 'r') as fh:
        lines = fh.readlines()

    with open('Driver.F90', 'w') as fh:

        for line in lines:
            if line[4:10] == 'mdot =':
                fh.write("    mdot = {0:E} * Msun / secyr\n".format(mdot))
            elif line[4:8] == 'dt =':
                fh.write("    dt = {0:f} * secyr\n".format(timestep))
            elif line[4:13] == 'maxtime =':
                fh.write("    maxtime = {0:E} * secyr\n".format(fulltime))
            else:
                fh.write(line)

def compile_code(program='all'):
    os.system('make {0}'.format(program))

def run_code(code='protostellar_evolution'):
    os.system('./{0}'.format(code))


def isothermal_sphere(mf, T=10):
    T1 = (T/10)
    mdot1 = 1.54e-6 * T1**1.5 # msun/yr
    mdot = mdot1

    # years
    tf1 = (1/mdot1)
    tf = tf1 * mf
    
    write_params(mdot=mdot, fulltime=tf, mf=mf)

def tc_write_params(ntimestep=1000, fulltime=None, mf=100):


    if fulltime is None:
        mdot1 = 4.9e-6 # normalized by surface density^3/4
        tf1 = 2./mdot1/1e6 # Myr
        tf = tf1 * mf**(0.25)
        fulltime = tf*1e6
        print("time to accrete {0} msun in tc model = {1} Myr".format(mf, tf))

    if fulltime < 2e6:
        fulltime = 2e6

    timestep = fulltime / ntimestep

    with open('TurbulentCoreDriver.F90', 'r') as fh:
        lines = fh.readlines()

    with open('TurbulentCoreDriver.F90', 'w') as fh:

        for line in lines:
            if line[4:12] == 'mfinal =':
                fh.write("    mfinal = {0:E}\n".format(mf))
            elif line[4:8] == 'dt =':
                fh.write("    dt = {0:f} * secyr\n".format(timestep))
            elif line[4:13] == 'maxtime =':
                fh.write("    maxtime = {0:E} * secyr\n".format(fulltime))
            else:
                fh.write(line)

def assemble_model_grid(prefix='turbulentcore_protostellar_evolution_m',
                        masses=(0.1,0.5,1,5,10,50), ntime=1000):

    from astropy.table import Table
    from astropy.io import fits

    grid = np.empty([len(masses), ntime, 9])

    for ii,mf in enumerate(masses):
        fn = "turbulentcore_protostellar_evolution_m={0}.txt".format(mf)
        tbl = Table.read(fn, format='ascii')

        grid[ii,:,0] = tbl['Time']
        grid[ii,:,1] = tbl['Stellar_Mass']
        grid[ii,:,2] = tbl['Accretion_Rate']
        grid[ii,:,3] = tbl['Stellar_Radius']
        grid[ii,:,4] = tbl['Polytropic_Index']
        grid[ii,:,5] = tbl['Deuterium_Mass']
        grid[ii,:,6] = tbl['Intrinsic_Lum']
        grid[ii,:,7] = tbl['Total_Luminosity']
        grid[ii,:,8] = tbl['Stage']


    hdr = fits.Header()
    hdr['COL0'] = 'Time'
    hdr['COL1'] = 'Stellar_Mass'
    hdr['COL2'] = 'Accretion_Rate'
    hdr['COL3'] = 'Stellar_Radius'
    hdr['COL4'] = 'Polytropic_Index'
    hdr['COL5'] = 'Deuterium_Mass'
    hdr['COL6'] = 'Intrinsic_Lum'
    hdr['COL7'] = 'Total_Luminosity'
    hdr['COL8'] = 'Stage'

    fits.writeto(filename='turbulent_grid.fits', data=grid, header=hdr)




if __name__ == "__main__":

    if False:
        for mdot in [1e-3, 3e-3, 1e-4, 1e-5, 1e-6]:
            os.system('git checkout 8cb810f -- Driver.F90')
            write_params(mdot=mdot)
            compile_code()
            run_code()
            shutil.move("protostellar_evolution.txt",
                        "protostellar_evolution_mdot={0}.txt".format(mdot))
    
    for mf in (0.1,0.5,1,5,10,50):
        os.system('git checkout cc6cf07 -- TurbulentCoreDriver.F90')
        tc_write_params(mf=mf, fulltime=2e6)
        compile_code('turbulentcore')
        run_code('tc_protostellar_evolution')
        shutil.move("turbulentcore_protostellar_evolution.txt",
                    "turbulentcore_protostellar_evolution_m={0}.txt".format(mf))
