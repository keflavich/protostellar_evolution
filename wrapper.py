import numpy as np
import os
import shutil

def write_params(mdot=1e-4, timestep=100, fulltime=None, mf=100):

    if fulltime is None:
        fulltime = mf / mdot

    timestep = fulltime / 1000

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

def compile_code():
    os.system('make')

def run_code():
    os.system('./protostellar_evolution')


def isothermal_sphere(mf, T=10):
    T1 = (T/10)
    mdot1 = 1.54e-6 * T1**1.5 # msun/yr
    mdot = mdot1

    # years
    tf1 = (1/mdot1)
    tf = tf1 * mf
    
    write_params(mdot=mdot, fulltime=tf, mf=mf)


if __name__ == "__main__":

    for mdot in [1e-3, 3e-3, 1e-4, 1e-5, 1e-6]:
        os.system('git checkout 8cb810f -- Driver.F90')
        write_params(mdot=mdot)
        compile_code()
        run_code()
        shutil.move("protostellar_evolution.txt",
                    "protostellar_evolution_mdot={0}.txt".format(mdot))
